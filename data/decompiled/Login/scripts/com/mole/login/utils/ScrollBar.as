package com.mole.login.utils
{
   import flash.display.*;
   import flash.events.*;
   import flash.geom.*;
   import flash.utils.*;
   
   public class ScrollBar extends EventDispatcher
   {
      
      private static var InstanceArray:Array = new Array();
      
      public static const ENABLE_VISIBLE:String = "visible";
      
      public static const ENABLE_ABATE:String = "abate";
      
      public static const DIRECTION_VERTICAL:String = "vertical";
      
      public static const DIRECTION_HORIZONTAL:String = "horizontal";
      
      public static const EVENT_ON_CHANGE:String = "Event_On_Change";
      
      public static const EVENT_ON_SIZE_CHANGE:String = "Event_On_Size_Change";
      
      private var bufferSize:Number;
      
      private var spaceSize:Number;
      
      private var currentSizeInt:int;
      
      private var scrollBar_Class:Class = ScrollBar_scrollBar_Class;
      
      private var autoClear:Boolean;
      
      private var scrollTimer:Timer;
      
      private var targetMC:*;
      
      private var scrollMC:*;
      
      private var bg_mc:MovieClip;
      
      private var line_mc:MovieClip;
      
      private var draw_btn:MovieClip;
      
      private var up_btn:SimpleButton;
      
      private var down_btn:SimpleButton;
      
      private var downBool:Boolean;
      
      private var moveTimer:Timer;
      
      private var mask:Shape;
      
      private var offsetNum:Number;
      
      private var width:Number;
      
      private var height:Number;
      
      private var originX:Number;
      
      private var originY:Number;
      
      private var targetX:Number;
      
      private var targetY:Number;
      
      private var posType:int;
      
      private var prop:Number;
      
      private var enableType:String;
      
      private var direction:String;
      
      public function ScrollBar(param1:MovieClip, param2:*, param3:* = 200, param4:String = "visible", param5:String = "vertical", param6:Number = 20, param7:Number = 0)
      {
         super();
         if(param2)
         {
            this.targetMC = param2;
            if(!param1)
            {
               this.scrollMC = new this.scrollBar_Class();
               this.autoClear = true;
            }
            else
            {
               this.scrollMC = param1;
               this.autoClear = false;
            }
            this.enableType = param4;
            this.direction = param5;
            this.bufferSize = param7;
            this.spaceSize = param6;
            this.bg_mc = this.scrollMC.bg_mc;
            this.line_mc = this.scrollMC.line_mc;
            this.draw_btn = this.scrollMC.draw_btn;
            this.up_btn = this.scrollMC.up_btn;
            this.down_btn = this.scrollMC.down_btn;
            this.downBool = false;
            this.posType = 0;
            this.currentSizeInt = 0;
            if(this.targetMC is MovieClip || this.targetMC is Sprite)
            {
               this.init(param3);
            }
            return;
         }
         throw new Error("目标不能为空!!");
      }
      
      public function init(param1:*) : void
      {
         var _loc6_:String = null;
         var _loc7_:Shape = null;
         var _loc2_:Object = {};
         if(!this.scrollMC.parent)
         {
            this.targetMC.parent.addChild(this.scrollMC);
         }
         var _loc3_:Number = 0;
         var _loc4_:Number = 0;
         if(typeof param1 == "object")
         {
            this.height = param1.length ? Number(param1.length) : 120;
            this.width = param1.size ? Number(param1.size) : 24;
            this.scrollMC.x = param1.x ? param1.x : 0;
            this.scrollMC.y = param1.y ? param1.y : 0;
         }
         else if(typeof param1 == "number")
         {
            this.width = 24;
            this.height = param1;
         }
         else
         {
            this.width = 24;
            this.height = 200;
         }
         _loc3_ = this.width;
         _loc4_ = this.height;
         this.originX = this.targetMC.x;
         this.originY = this.targetMC.y;
         this.bg_mc.width = _loc3_;
         this.draw_btn.width = _loc3_;
         this.draw_btn.x = 0;
         this.draw_btn.y = _loc3_;
         this.line_mc.width = _loc3_;
         this.line_mc.x = 0;
         this.up_btn.width = _loc3_;
         this.up_btn.x = 0;
         this.up_btn.y = 0;
         this.up_btn.height = _loc3_;
         this.down_btn.width = _loc3_;
         this.down_btn.x = 0;
         this.down_btn.height = _loc3_;
         this.line_mc.mouseEnabled = false;
         var _loc5_:Number = this.down_btn.height + this.up_btn.height + 8;
         if(_loc4_ < _loc5_)
         {
            this.draw_btn.height = 4;
            this.down_btn.y = _loc5_;
            this.bg_mc.height = _loc5_;
         }
         else
         {
            this.draw_btn.height = (this.bg_mc.height - _loc5_ + 5) / this.targetMC.height * (this.bg_mc.height - _loc5_ + 5);
            this.down_btn.y = this.height;
            this.bg_mc.height = _loc4_;
         }
         for(_loc6_ in InstanceArray)
         {
            _loc2_ = InstanceArray[_loc6_];
            if(!_loc2_.targetMC.stage || !_loc2_.mask.stage)
            {
               InstanceArray.splice(_loc6_,1);
            }
         }
         for(_loc6_ in InstanceArray)
         {
            _loc2_ = InstanceArray[_loc6_];
            if(_loc2_.targetMC == this.targetMC)
            {
               _loc7_ = _loc2_.mask;
               break;
            }
         }
         if(this.direction == "vertical")
         {
            if(!_loc7_)
            {
               this.mask = this.createRectangle(0,0,this.scrollMC.x - this.targetMC.x,_loc4_);
               this.mask.x = this.targetMC.x;
               this.mask.y = this.targetMC.y;
               this.targetMC.parent.addChild(this.mask);
               this.targetMC.mask = this.mask;
               _loc2_.targetMC = this.targetMC;
               _loc2_.mask = this.mask;
               _loc2_.scrollMC = this.scrollMC;
               _loc2_.direction = this.direction;
               InstanceArray.push(_loc2_);
            }
            else
            {
               this.mask = _loc7_;
               this.mask.height = _loc4_;
            }
            this.mask.y = this.scrollMC.y;
         }
         else
         {
            this.scrollMC.rotation = -90;
            this.scrollMC.x = this.targetMC.x;
            if(!_loc7_)
            {
               this.mask = this.createRectangle(0,0,_loc4_,this.scrollMC.y - this.targetMC.y - this.width);
               this.mask.x = this.targetMC.x;
               this.mask.y = this.targetMC.y;
               this.targetMC.parent.addChild(this.mask);
               this.targetMC.mask = this.mask;
               _loc2_.targetMC = this.targetMC;
               _loc2_.mask = this.mask;
               _loc2_.scrollMC = this.scrollMC;
               _loc2_.direction = this.direction;
               InstanceArray.push(_loc2_);
            }
            else
            {
               this.mask = _loc7_;
               this.mask.width = _loc4_;
            }
            this.mask.x = this.scrollMC.x;
         }
         BC.addEvent(this,this.up_btn,MouseEvent.MOUSE_DOWN,this.setup);
         BC.addEvent(this,this.down_btn,MouseEvent.MOUSE_DOWN,this.setdown);
         BC.addEvent(this,this.draw_btn,MouseEvent.MOUSE_DOWN,this.drawBtnDown);
         BC.addEvent(this,this.bg_mc,MouseEvent.MOUSE_DOWN,this.bgBtnDown);
         if(this.targetMC.stage)
         {
            BC.addEvent(this,this.targetMC.stage,MouseEvent.MOUSE_WHEEL,this.onMouseWheel);
         }
         BC.addEvent(this,this.targetMC,Event.REMOVED_FROM_STAGE,this.clearClass);
         this.moveTimer = new Timer(25,0);
         this.doChange();
      }
      
      public function sendToTop() : void
      {
         if(this.downBool)
         {
            this.posType = 0;
         }
         else
         {
            this.posType = 1;
         }
         this.doChange();
      }
      
      public function sendToBottom() : void
      {
         if(this.downBool)
         {
            this.posType = 0;
         }
         else
         {
            this.posType = 2;
         }
         this.doChange();
      }
      
      public function set visible(param1:Boolean) : void
      {
         this.scrollMC.visible = param1;
      }
      
      public function set alpha(param1:Number) : void
      {
         this.scrollMC.alpha = param1;
      }
      
      public function get visible() : Boolean
      {
         return this.targetMC.visible;
      }
      
      public function AddupBtn_proxy(param1:*) : void
      {
         BC.addEvent(this,param1,MouseEvent.MOUSE_DOWN,this.setup);
      }
      
      public function DelupBtn_proxy(param1:*) : void
      {
         BC.removeEvent(this,param1,MouseEvent.MOUSE_DOWN,this.setup);
      }
      
      public function AdddownBtn_proxy(param1:*) : void
      {
         BC.addEvent(this,param1,MouseEvent.MOUSE_DOWN,this.setdown);
      }
      
      public function DeldownBtn_proxy(param1:*) : void
      {
         BC.removeEvent(this,param1,MouseEvent.MOUSE_DOWN,this.setdown);
      }
      
      public function checkScrollTimeout(param1:Event) : void
      {
         var _loc2_:int = this.scrollMC.globalToLocal(new Point(this.targetMC.stage.mouseX,this.targetMC.stage.mouseY)).y - this.draw_btn.y;
         var _loc3_:int = this.spaceSize / 2;
         if(_loc2_ < _loc3_ && _loc2_ > -_loc3_)
         {
            this.scrollTimeout();
         }
      }
      
      public function scrollTimeout(param1:MouseEvent = null) : void
      {
         GC.clearGTimeout(this.scrollTimer);
         BC.removeEvent(this,this.targetMC.stage,MouseEvent.MOUSE_UP,this.scrollTimeout);
         BC.removeEvent(this,this,EVENT_ON_CHANGE,this.checkScrollTimeout);
      }
      
      public function gettargetMC() : *
      {
         return this.targetMC;
      }
      
      public function getScrollMC() : *
      {
         return this.scrollMC;
      }
      
      public function setup(param1:*) : void
      {
         var size:Number;
         var currentPosSize:int;
         var addSize:Number;
         var delay:Number = Number(NaN);
         var E:* = param1;
         var lenNum:Number = 0;
         if(E is MouseEvent)
         {
            if(E.currentTarget == this.bg_mc)
            {
               lenNum = this.spaceSize * 2;
            }
            else
            {
               lenNum = this.spaceSize;
            }
            delay = lenNum;
            BC.addEvent(this,this.targetMC.stage,MouseEvent.MOUSE_UP,this.scrollTimeout);
            BC.addEvent(this,this,EVENT_ON_CHANGE,this.checkScrollTimeout);
            GC.clearGTimeout(this.scrollTimer);
            this.scrollTimer = GC.setGTimeout(function():*
            {
               scrollTimer = GC.setGInterval(setup,80,delay);
            },400);
         }
         else if(Boolean(E) && E is Number)
         {
            lenNum = E;
         }
         else
         {
            lenNum = this.spaceSize;
         }
         size = this.prop ? this.spaceSize / this.prop : 0;
         currentPosSize = Math.round((this.draw_btn.y - this.width) / size);
         addSize = lenNum / this.spaceSize;
         lenNum = (int(currentPosSize - addSize)) * size + this.width;
         this.draw_btn.y = lenNum;
         this.checkDrawBtn();
         this.doChange();
      }
      
      public function setdown(param1:*) : void
      {
         var size:Number;
         var currentPosSize:int;
         var addSize:Number;
         var delay:Number = Number(NaN);
         var E:* = param1;
         var lenNum:Number = 0;
         if(E is MouseEvent)
         {
            if(E.currentTarget == this.bg_mc)
            {
               lenNum = this.spaceSize * 2;
            }
            else
            {
               lenNum = this.spaceSize;
            }
            delay = lenNum;
            BC.addEvent(this,this.targetMC.stage,MouseEvent.MOUSE_UP,this.scrollTimeout);
            BC.addEvent(this,this,EVENT_ON_CHANGE,this.checkScrollTimeout);
            GC.clearGTimeout(this.scrollTimer);
            this.scrollTimer = GC.setGTimeout(function():*
            {
               scrollTimer = GC.setGInterval(setdown,80,delay);
            },400);
         }
         else if(Boolean(E) && E is Number)
         {
            lenNum = E;
         }
         else
         {
            lenNum = this.spaceSize;
         }
         size = this.prop ? this.spaceSize / this.prop : 0;
         currentPosSize = Math.round((this.draw_btn.y - this.width) / size);
         addSize = lenNum / this.spaceSize;
         lenNum = (int(currentPosSize + addSize)) * size + this.width;
         this.draw_btn.y = lenNum;
         this.checkDrawBtn();
         this.doChange();
      }
      
      public function ScrollToItem(param1:Object) : void
      {
         var _loc3_:int = 0;
         var _loc4_:Array = null;
         var _loc5_:* = undefined;
         var _loc6_:int = 0;
         var _loc7_:Number = Number(NaN);
         var _loc8_:DisplayObject = null;
         var _loc2_:Number = 0;
         if(Boolean(param1) && param1.hasOwnProperty("y"))
         {
            _loc3_ = int(this.targetMC.numChildren);
            _loc4_ = new Array();
            _loc6_ = 0;
            while(_loc6_ < _loc3_)
            {
               _loc8_ = this.targetMC.getChildAt(_loc6_);
               _loc4_.push(_loc8_);
               if(_loc8_ == param1)
               {
                  _loc5_ = _loc8_;
               }
               _loc6_++;
            }
            _loc4_.sortOn("y",Array.NUMERIC);
            _loc7_ = this.prop ? this.spaceSize / this.prop : 0;
            this.draw_btn.y = _loc4_.indexOf(_loc5_) * _loc7_ + this.width;
            this.checkDrawBtn();
            this.doChange();
            return;
         }
      }
      
      public function doChange() : void
      {
         var _loc1_:Number = Number(NaN);
         var _loc2_:Number = Number(NaN);
         var _loc3_:Number = Number(NaN);
         var _loc4_:Number = Number(NaN);
         var _loc5_:Number = Number(NaN);
         var _loc6_:Number = Number(NaN);
         var _loc7_:int = this.currentSizeInt;
         if(this.direction == "vertical")
         {
            this.mask.y = this.scrollMC.y;
            this.mask.height = this.height;
            _loc6_ = this.height - this.width * 2;
            _loc2_ = _loc6_ / this.targetMC.height * _loc6_;
            this.draw_btn.height = _loc2_ > 8 ? _loc2_ : 8;
            if(this.targetMC.height <= this.height)
            {
               this.prop = 0;
               this.enableScroll(true);
            }
            else
            {
               this.prop = (this.targetMC.height - this.height) / (this.height - this.width * 2 - this.draw_btn.height);
               this.enableScroll(false);
            }
            this.draw_btn.height = this.draw_btn.height > _loc6_ ? _loc6_ : this.draw_btn.height;
            _loc5_ = this.height - this.width - this.draw_btn.height;
            _loc4_ = this.width;
            if(this.posType == 1)
            {
               this.draw_btn.y = _loc4_;
            }
            else if(this.posType == 2)
            {
               this.draw_btn.y = _loc5_;
            }
            else
            {
               if(this.draw_btn.y > _loc5_)
               {
                  this.draw_btn.y = _loc5_;
               }
               if(this.draw_btn.y < _loc4_)
               {
                  this.draw_btn.y == _loc4_;
               }
            }
            if(this.bufferSize > 0)
            {
               this.targetY = -(this.draw_btn.y - this.width) * this.prop + this.originY;
               if(!this.moveTimer.running)
               {
                  BC.addEvent(this,this.moveTimer,TimerEvent.TIMER,this.bufferTimerY);
                  this.moveTimer.start();
               }
            }
            else
            {
               this.targetMC.y = -(this.draw_btn.y - this.width) * this.prop + this.originY;
            }
            this.currentSizeInt = this.targetMC.y / this.spaceSize;
         }
         else
         {
            this.mask.x = this.scrollMC.x;
            this.mask.width = this.height;
            _loc6_ = this.height - this.width * 2;
            _loc3_ = _loc6_ / this.targetMC.width * _loc6_;
            this.draw_btn.height = _loc3_ > 8 ? _loc3_ : 8;
            if(this.targetMC.width <= this.height)
            {
               this.prop = 0;
               this.enableScroll(true);
            }
            else
            {
               this.prop = (this.targetMC.width - this.height) / (this.height - this.width * 2 - this.draw_btn.height);
               this.enableScroll(false);
            }
            this.draw_btn.height = this.draw_btn.height > _loc6_ ? _loc6_ : this.draw_btn.height;
            _loc5_ = this.height - this.width - this.draw_btn.height;
            _loc4_ = this.width;
            if(this.posType == 1)
            {
               this.draw_btn.y = _loc4_;
            }
            else if(this.posType == 2)
            {
               this.draw_btn.y = _loc5_;
            }
            else
            {
               if(this.draw_btn.y > _loc5_)
               {
                  this.draw_btn.y = _loc5_;
               }
               if(this.draw_btn.y < _loc4_)
               {
                  this.draw_btn.y == _loc4_;
               }
            }
            if(this.bufferSize > 0)
            {
               this.targetX = -(this.draw_btn.y - this.width) * this.prop + this.originX;
               if(!this.moveTimer.running)
               {
                  BC.addEvent(this,this.moveTimer,TimerEvent.TIMER,this.bufferTimerX);
                  this.moveTimer.start();
               }
            }
            else
            {
               this.targetMC.x = -(this.draw_btn.y - this.width) * this.prop + this.originX;
            }
            this.currentSizeInt = this.targetMC.x / this.spaceSize;
         }
         this.line_mc.y = int(this.draw_btn.y + this.draw_btn.height / 2);
         this.posType = 0;
         if(this.currentSizeInt != _loc7_)
         {
            dispatchEvent(new Event(EVENT_ON_SIZE_CHANGE));
         }
         dispatchEvent(new Event(EVENT_ON_CHANGE));
      }
      
      private function onMouseWheel(param1:MouseEvent) : void
      {
         var _loc4_:int = 0;
         var _loc2_:Boolean = Boolean(this.targetMC.hitTestPoint(this.scrollMC.stage.mouseX,this.scrollMC.stage.mouseY,false));
         var _loc3_:Boolean = Boolean(this.scrollMC.hitTestPoint(this.scrollMC.stage.mouseX,this.scrollMC.stage.mouseY,false));
         if(_loc2_ || _loc3_)
         {
            _loc4_ = param1.delta;
            if(_loc4_ > 0)
            {
               this.setup(this.spaceSize);
            }
            else
            {
               this.setdown(this.spaceSize);
            }
         }
      }
      
      private function drawBtnDown(param1:MouseEvent) : void
      {
         this.offsetNum = this.scrollMC.globalToLocal(new Point(param1.stageX,param1.stageY)).y - this.draw_btn.y;
         BC.addEvent(this,this.scrollMC.stage,MouseEvent.MOUSE_MOVE,this.drawBtnMove);
         BC.addEvent(this,this.scrollMC.stage,MouseEvent.MOUSE_UP,this.drawBtnUp);
         this.downBool = true;
         this.doChange();
      }
      
      private function drawBtnMove(param1:MouseEvent) : void
      {
         this.draw_btn.y = this.scrollMC.globalToLocal(new Point(param1.stageX,param1.stageY)).y - this.offsetNum;
         this.checkDrawBtn();
         this.doChange();
      }
      
      private function drawBtnUp(param1:MouseEvent) : void
      {
         BC.removeEvent(this,this.scrollMC.stage,MouseEvent.MOUSE_MOVE,this.drawBtnMove);
         BC.removeEvent(this,this.scrollMC.stage,MouseEvent.MOUSE_UP,this.drawBtnUp);
         this.downBool = false;
         this.doChange();
      }
      
      private function bgBtnDown(param1:MouseEvent) : void
      {
         if(this.scrollMC.globalToLocal(new Point(param1.stageX,param1.stageY)).y < this.draw_btn.y)
         {
            this.setup(param1);
         }
         else
         {
            this.setdown(param1);
         }
      }
      
      private function checkDrawBtn() : void
      {
         var _loc1_:Number = this.height - this.width - this.draw_btn.height;
         this.draw_btn.y = this.draw_btn.y <= this.width ? this.width : (this.draw_btn.y >= _loc1_ ? _loc1_ : this.draw_btn.y);
      }
      
      private function createRectangle(param1:Number, param2:Number, param3:Number, param4:Number) : Shape
      {
         var _loc5_:Shape = new Shape();
         _loc5_.graphics.beginFill(255,0);
         _loc5_.graphics.drawRect(param1,param2,param3,param4);
         _loc5_.graphics.endFill();
         return _loc5_;
      }
      
      private function enableScroll(param1:Boolean) : void
      {
         if(param1)
         {
            this.scrollMC.mouseChildren = false;
            this.draw_btn.visible = false;
            this.line_mc.visible = false;
            if(this.enableType == "visible")
            {
               this.scrollMC.visible = false;
            }
            else
            {
               this.up_btn.alpha = 0.5;
               this.down_btn.alpha = 0.5;
            }
            this.line_mc.y = this.draw_btn.y + this.width + this.width / 2;
         }
         else
         {
            this.scrollMC.mouseChildren = true;
            this.draw_btn.alpha = 1;
            this.draw_btn.visible = true;
            this.line_mc.visible = true;
            if(this.enableType == "visible")
            {
               this.scrollMC.visible = true;
            }
            else
            {
               this.up_btn.alpha = 1;
               this.down_btn.alpha = 1;
            }
         }
      }
      
      private function bufferTimerX(param1:TimerEvent) : void
      {
         var _loc2_:Number = this.targetX - this.targetMC.x;
         this.targetMC.x += _loc2_ / this.bufferSize;
         if(int(_loc2_ * 3) == 0)
         {
            this.targetMC.x = this.targetX;
            this.moveTimer.stop();
            BC.removeEvent(this,this.moveTimer,TimerEvent.TIMER);
         }
      }
      
      private function bufferTimerY(param1:TimerEvent) : void
      {
         var _loc2_:Number = this.targetY - this.targetMC.y;
         this.targetMC.y += _loc2_ / this.bufferSize;
         if(int(_loc2_ * 3) == 0)
         {
            this.targetMC.y = this.targetY;
            this.moveTimer.stop();
            BC.removeEvent(this,this.moveTimer,TimerEvent.TIMER);
         }
      }
      
      public function clearClass(param1:* = null) : void
      {
         var _loc2_:Object = null;
         var _loc3_:String = null;
         BC.removeEvent(this);
         GC.clearGTimeout(this.scrollTimer);
         for(_loc3_ in InstanceArray)
         {
            _loc2_ = InstanceArray[_loc3_];
            if(_loc2_.targetMC == this.targetMC && _loc2_.scrollMC == this.scrollMC)
            {
               if(_loc2_.mask.parent)
               {
                  _loc2_.mask.parent.removeChild(_loc2_.mask);
               }
               InstanceArray.splice(_loc3_,1);
            }
         }
         if(this.autoClear && Boolean(this.scrollMC) && Boolean(this.scrollMC.parent))
         {
            this.scrollMC.parent.removeChild(this.scrollMC);
         }
         this.targetMC = null;
         this.scrollMC = null;
         this.bg_mc = null;
         this.line_mc = null;
         this.draw_btn = null;
         this.up_btn = null;
         this.down_btn = null;
         this.mask = null;
      }
   }
}

