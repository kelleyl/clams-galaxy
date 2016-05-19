define([],function(){var a=Backbone.View.extend({initialize:function(a){this.setElement($("<div/>").addClass("corner").addClass("frame")),this.$el.append(this.$header=$("<div/>").addClass("f-header corner").append(this.$title=$("<div/>").addClass("f-title").html(a.title||"")).append(this.$close=$("<div/>").addClass("f-icon f-close fa fa-close")).append(this.$pin=$("<div/>").addClass("f-icon f-pin fa fa-thumb-tack")).append(this.$left=$("<div/>").addClass("f-icon f-left fa fa-chevron-circle-left")).append(this.$right=$("<div/>").addClass("f-icon f-right fa fa-chevron-circle-right"))).append(this.$content=$("<div/>").addClass("f-content").append($("<div/>").addClass("f-cover"))).append(this.$resize=$("<div/>").addClass("f-resize f-icon corner fa fa-expand")),a.onslider&&this.$left.on("click",function(){a.onslider()}),a.url?this.$content.append($("<iframe/>").addClass("f-iframe").attr("scrolling","auto").attr("src",a.url+(-1===a.url.indexOf("?")?"?":"&")+"widget=True")):a.content&&(_.isFunction(a.content)?a.content(this.$content):this.$content.append(a.content))}}),b=Backbone.View.extend({defaultOptions:{frame:{cols:6,rows:3},rows:1e3,cell:130,margin:5,scroll:5,top_min:40,frame_max:9,visible:!0},cols:0,top:0,top_max:0,frame_z:0,frame_counter:0,frame_uid:0,frame_list:{},frame_shadow:null,visible:!1,event:{},initialize:function(a){var b=this;this.options=_.defaults(a||{},this.defaultOptions),this.visible=this.options.visible,this.top=this.top_max=this.options.top_min,this.setElement($("<div/>").addClass("galaxy-frame").append($("<div/>").addClass("frame-background")).append($("<div/>").addClass("frame-menu frame-scroll-up fa fa-chevron-up fa-2x")).append($("<div/>").addClass("frame-menu frame-scroll-down fa fa-chevron-down fa-2x"))),this.frame_shadow=new Backbone.View({}).setElement($("<div/>").addClass("corner frame-shadow")),this.$el.append(this.frame_shadow.$el),this._frameInit(this.frame_shadow,"#frame-shadow"),this._frameResize(this.frame_shadow,{width:0,height:0}),this.frame_list["#frame-shadow"]=this.frame_shadow,this.visible?this.show():this.hide(),this._panelRefresh(),$(window).resize(function(){b.visible&&b._panelRefresh()})},render:function(){this.$(".frame-scroll-up")[this.top!=this.options.top_min&&"show"||"hide"](),this.$(".frame-scroll-down")[this.top!=this.top_max&&"show"||"hide"]()},add:function(b){if(this.frame_counter>=this.options.frame_max)Galaxy.modal.show({title:"Warning",body:"You have reached the maximum number of allowed frames ("+this.options.frame_max+").",buttons:{Close:function(){Galaxy.modal.hide()}}});else{var c="#frame-"+this.frame_uid++;if(0!==$(c).length)Galaxy.modal.show({title:"Error",body:"This frame already exists. This page might contain multiple frame managers.",buttons:{Close:function(){Galaxy.modal.hide()}}});else{this.top=this.options.top_min;var d=new a(b);this.$el.append(d.$el),b.width=this._toPixelCoord("width",this.options.frame.cols),b.height=this._toPixelCoord("height",this.options.frame.rows),this.frame_z=parseInt(d.$el.css("z-index")),this.frame_list[c]=d,this.frame_counter++,this._frameInit(d,c),this._frameResize(d,{width:b.width,height:b.height}),this._frameInsert(d,{top:0,left:0},!0),!this.visible&&this.show(),this.trigger("add")}}},del:function(a){var b=this,c=a.$el;c.fadeOut("fast",function(){c.remove(),delete b.frame_list[a.id],b.frame_counter--,b._panelRefresh(!0),b._panelAnimationComplete(),b.trigger("remove")})},show:function(){this.visible=!0,this.$el.fadeIn("fast"),this.trigger("show")},hide:function(){this.event.type||(this.visible=!1,this.$el.fadeOut("fast",function(){$(this).hide()}),this.trigger("hide"))},length:function(){return this.frame_counter},events:{mousemove:"_eventFrameMouseMove",mouseup:"_eventFrameMouseUp",mouseleave:"_eventFrameMouseUp",mousewheel:"_eventPanelScroll",DOMMouseScroll:"_eventPanelScroll","mousedown .frame":"_eventFrameMouseDown","mousedown .frame-background":"_eventHide","mousedown .frame-scroll-up":"_eventPanelScroll_up","mousedown .frame-scroll-down":"_eventPanelScroll_down","mousedown .f-close":"_eventFrameClose","mousedown .f-pin":"_eventFrameLock"},_eventFrameMouseDown:function(a){if(!this.event.type&&(($(a.target).hasClass("f-header")||$(a.target).hasClass("f-title"))&&(this.event.type="drag"),$(a.target).hasClass("f-resize")&&(this.event.type="resize"),this.event.type)){if(a.preventDefault(),this.event.target=this._frameIdentify(a.target),this.event.target.grid_lock)return void(this.event.type=null);this.event.xy={x:a.originalEvent.pageX,y:a.originalEvent.pageY},this._frameDragStart(this.event.target)}},_eventFrameMouseMove:function(a){if(this.event.type){var b={x:a.originalEvent.pageX,y:a.originalEvent.pageY},c={x:b.x-this.event.xy.x,y:b.y-this.event.xy.y};this.event.xy=b;var d=this._frameScreen(this.event.target);if("resize"==this.event.type){d.width+=c.x,d.height+=c.y;var e=this.options.cell-this.options.margin-1;d.width=Math.max(d.width,e),d.height=Math.max(d.height,e),this._frameResize(this.event.target,d),d.width=this._toGridCoord("width",d.width)+1,d.height=this._toGridCoord("height",d.height)+1,d.width=this._toPixelCoord("width",d.width),d.height=this._toPixelCoord("height",d.height),this._frameResize(this.frame_shadow,d),this._frameInsert(this.frame_shadow,{top:this._toGridCoord("top",d.top),left:this._toGridCoord("left",d.left)})}else if("drag"==this.event.type){d.left+=c.x,d.top+=c.y,this._frameOffset(this.event.target,d);var f={top:this._toGridCoord("top",d.top),left:this._toGridCoord("left",d.left)};0!==f.left&&f.left++,this._frameInsert(this.frame_shadow,f)}}},_eventFrameMouseUp:function(){this.event.type&&(this._frameDragStop(this.event.target),this.event.type=null)},_eventFrameClose:function(a){this.event.type||(a.preventDefault(),this.del(this._frameIdentify(a.target)))},_eventFrameLock:function(a){if(!this.event.type){a.preventDefault();var b=this._frameIdentify(a.target),c=b.grid_lock=!b.grid_lock,d=b.$el;d.find(".f-pin")[c?"addClass":"removeClass"]("toggle"),d.find(".f-header")[c?"removeClass":"addClass"]("f-not-allowed"),d.find(".f-title")[c?"removeClass":"addClass"]("f-not-allowed"),d.find(".f-resize")[c?"hide":"show"](),d.find(".f-close")[c?"hide":"show"]()}},_eventHide:function(){!this.event.type&&this.hide()},_eventPanelScroll:function(a){if(!this.event.type&&this.visible){var b=$(a.srcElement).parents(".frame");0!==b.length?a.stopPropagation():(a.preventDefault(),this._panelScroll(a.originalEvent.detail?a.originalEvent.detail:a.originalEvent.wheelDelta/-3))}},_eventPanelScroll_up:function(a){this.event.type||(a.preventDefault(),this._panelScroll(-this.options.scroll))},_eventPanelScroll_down:function(a){this.event.type||(a.preventDefault(),this._panelScroll(this.options.scroll))},_frameInit:function(a,b){a.id=b,a.screen_location={},a.grid_location={},a.grid_rank=null,a.grid_lock=!1,a.$el.attr("id",b.substring(1))},_frameIdentify:function(a){return this.frame_list["#"+$(a).closest(".frame").attr("id")]},_frameDragStart:function(a){this._frameFocus(a,!0);var b=this._frameScreen(a);this._frameResize(this.frame_shadow,b),this._frameGrid(this.frame_shadow,a.grid_location),a.grid_location=null,this.frame_shadow.$el.show(),$(".f-cover").show()},_frameDragStop:function(a){this._frameFocus(a,!1);var b=this._frameScreen(this.frame_shadow);this._frameResize(a,b),this._frameGrid(a,this.frame_shadow.grid_location,!0),this.frame_shadow.grid_location=null,this.frame_shadow.$el.hide(),$(".f-cover").hide(),this._panelAnimationComplete()},_toGridCoord:function(a,b){var c="width"==a||"height"==a?1:-1;return"top"==a&&(b-=this.top),parseInt((b+c*this.options.margin)/this.options.cell,10)},_toPixelCoord:function(a,b){var c="width"==a||"height"==a?1:-1,d=b*this.options.cell-c*this.options.margin;return"top"==a&&(d+=this.top),d},_toGrid:function(a){return{top:this._toGridCoord("top",a.top),left:this._toGridCoord("left",a.left),width:this._toGridCoord("width",a.width),height:this._toGridCoord("height",a.height)}},_toPixel:function(a){return{top:this._toPixelCoord("top",a.top),left:this._toPixelCoord("left",a.left),width:this._toPixelCoord("width",a.width),height:this._toPixelCoord("height",a.height)}},_isCollision:function(a){function b(a,b){return!(a.left>b.left+b.width-1||a.left+a.width-1<b.left||a.top>b.top+b.height-1||a.top+a.height-1<b.top)}for(var c in this.frame_list){var d=this.frame_list[c];if(null!==d.grid_location&&b(a,d.grid_location))return!0}return!1},_locationRank:function(a){return a.top*this.cols+a.left},_panelRefresh:function(a){this.cols=parseInt($(window).width()/this.options.cell,10)+1,this._frameInsert(null,null,a)},_panelAnimationComplete:function(){var a=this;$(".frame").promise().done(function(){a._panelScroll(0,!0)})},_panelScroll:function(a,b){var c=this.top-this.options.scroll*a;if(c=Math.max(c,this.top_max),c=Math.min(c,this.options.top_min),this.top!=c){for(var d in this.frame_list){var e=this.frame_list[d];if(null!==e.grid_location){var f={top:e.screen_location.top-(this.top-c),left:e.screen_location.left};this._frameOffset(e,f,b)}}this.top=c}this.render()},_frameInsert:function(a,b,c){var d=this,e=[];a&&(a.grid_location=null,e.push([a,this._locationRank(b)])),_.each(this.frame_list,function(a){null===a.grid_location||a.grid_lock||(a.grid_location=null,e.push([a,a.grid_rank]))}),e.sort(function(a,b){return a[1]<b[1]?-1:a[1]>b[1]?1:0}),_.each(e,function(a){d._framePlace(a[0],c)}),this.top_max=0,_.each(this.frame_list,function(a){null!==a.grid_location&&(d.top_max=Math.max(d.top_max,a.grid_location.top+a.grid_location.height))}),this.top_max=$(window).height()-this.top_max*this.options.cell-2*this.options.margin,this.top_max=Math.min(this.top_max,this.options.top_min),this.render()},_framePlace:function(a,b){a.grid_location=null;for(var c=this._toGrid(this._frameScreen(a)),d=!1,e=0;e<this.options.rows;e++){for(var f=0;f<Math.max(1,this.cols-c.width);f++)if(c.top=e,c.left=f,!this._isCollision(c)){d=!0;break}if(d)break}d?this._frameGrid(a,c,b):console.log("Grid dimensions exceeded.")},_frameFocus:function(a,b){a.$el.css("z-index",this.frame_z+(b?1:0))},_frameOffset:function(a,b,c){if(a.screen_location.left=b.left,a.screen_location.top=b.top,c){this._frameFocus(a,!0);var d=this;a.$el.animate({top:b.top,left:b.left},"fast",function(){d._frameFocus(a,!1)})}else a.$el.css({top:b.top,left:b.left})},_frameResize:function(a,b){a.$el.css({width:b.width,height:b.height}),a.screen_location.width=b.width,a.screen_location.height=b.height},_frameGrid:function(a,b,c){a.grid_location=b,this._frameOffset(a,this._toPixel(b),c),a.grid_rank=this._locationRank(b)},_frameScreen:function(a){var b=a.screen_location;return{top:b.top,left:b.left,width:b.width,height:b.height}}});return{View:b}});
//# sourceMappingURL=../../../maps/mvc/ui/ui-frames.js.map