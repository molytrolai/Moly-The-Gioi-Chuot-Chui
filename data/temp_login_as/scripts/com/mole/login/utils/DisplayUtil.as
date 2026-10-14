package com.mole.login.utils
{
   import flash.display.*;
   import flash.events.*;
   import flash.geom.*;
   import flash.text.*;
   
   public class DisplayUtil
   {
      
      private static const MOUSE_EVENT_LIST:Array = [MouseEvent.CLICK,MouseEvent.DOUBLE_CLICK,MouseEvent.MOUSE_DOWN,MouseEvent.MOUSE_MOVE,MouseEvent.MOUSE_OUT,MouseEvent.MOUSE_OVER,MouseEvent.MOUSE_UP,MouseEvent.MOUSE_WHEEL,MouseEvent.ROLL_OUT,MouseEvent.ROLL_OVER];
      
      public function DisplayUtil()
      {
         super();
      }
      
      public static function stopAllMovieClip(param1:DisplayObjectContainer, param2:uint = 0) : void
      {
         var _loc3_:MovieClip = null;
         var _loc4_:DisplayObjectContainer = null;
         var _loc5_:uint = 0;
         var _loc6_:uint = 0;
         if(Boolean(param1) && !(param1 is Loader))
         {
            _loc3_ = param1 as MovieClip;
            if(_loc3_)
            {
               if(param2 > 0)
               {
                  _loc3_.gotoAndStop(param2);
               }
               else
               {
                  _loc3_.stop();
               }
            }
            _loc5_ = uint(param1.numChildren);
            _loc6_ = 0;
            while(_loc6_ < _loc5_)
            {
               _loc4_ = param1.getChildAt(_loc6_) as DisplayObjectContainer;
               if(_loc4_ != null)
               {
                  stopAllMovieClip(_loc4_,param2);
               }
               _loc6_++;
            }
         }
      }
      
      public static function playAllMovieClip(param1:DisplayObjectContainer) : void
      {
         var _loc2_:MovieClip = null;
         var _loc3_:int = 0;
         var _loc4_:DisplayObjectContainer = null;
         var _loc5_:* = 0;
         if(Boolean(param1) && !(param1 is Loader))
         {
            _loc2_ = param1 as MovieClip;
            if(_loc2_ != null)
            {
               _loc2_.gotoAndPlay(1);
               _loc2_ = null;
            }
            _loc3_ = param1.numChildren - 1;
            if(_loc3_ < 0)
            {
               return;
            }
            _loc5_ = _loc3_;
            while(_loc5_ >= 0)
            {
               _loc4_ = param1.getChildAt(_loc5_) as DisplayObjectContainer;
               if(_loc4_ != null)
               {
                  playAllMovieClip(_loc4_);
               }
               _loc5_--;
            }
         }
      }
      
      public static function removeAllChild(param1:DisplayObjectContainer) : void
      {
         var _loc2_:DisplayObjectContainer = null;
         if(Boolean(param1) && !(param1 is Loader))
         {
            while(param1.numChildren > 0)
            {
               _loc2_ = param1.removeChildAt(0) as DisplayObjectContainer;
               if(_loc2_ != null)
               {
                  stopAllMovieClip(_loc2_);
                  _loc2_ = null;
               }
            }
         }
      }
      
      public static function removeForParent(param1:DisplayObject, param2:Boolean = true) : void
      {
         var disc:DisplayObjectContainer = null;
         var dis:DisplayObject = param1;
         var gc:Boolean = param2;
         if(dis == null)
         {
            return;
         }
         if(gc)
         {
            disc = dis as DisplayObjectContainer;
            if(disc)
            {
               stopAllMovieClip(disc);
               disc = null;
            }
         }
         if(!(dis.parent is Loader) && dis.parent != null)
         {
            try
            {
               dis.parent.removeChild(dis);
            }
            catch(e:Error)
            {
            }
         }
      }
      
      public static function hasParent(param1:DisplayObject) : Boolean
      {
         if(param1.parent == null)
         {
            return false;
         }
         return param1.parent.contains(param1);
      }
      
      public static function localToLocal(param1:DisplayObject, param2:DisplayObject, param3:Point = null) : Point
      {
         if(param3 == null)
         {
            param3 = new Point(0,0);
         }
         param3 = param1.localToGlobal(param3);
         return param2.globalToLocal(param3);
      }
      
      public static function align(param1:DisplayObject, param2:Rectangle = null, param3:int = 0, param4:Point = null) : void
      {
         var _loc5_:Rectangle = null;
         if(param2 == null)
         {
            if(!param1.stage)
            {
               param1.addEventListener(Event.ADDED_TO_STAGE,Delegate.create(onAddStage,param3,param4),false,0,true);
               return;
            }
            _loc5_ = new Rectangle(0,0,param1.stage.stageWidth,param1.stage.stageHeight);
         }
         else
         {
            _loc5_ = param2.clone();
         }
         align2(param1,_loc5_,param3,param4);
      }
      
      private static function onAddStage(param1:Event, param2:int, param3:Point) : void
      {
         var _loc5_:DisplayObject = param1.currentTarget as DisplayObject;
         _loc5_.removeEventListener(Event.ADDED_TO_STAGE,arguments.callee);
         align2(_loc5_,new Rectangle(0,0,_loc5_.stage.stageWidth,_loc5_.stage.stageHeight),param2,param3);
      }
      
      private static function align2(param1:DisplayObject, param2:Rectangle, param3:int, param4:Point) : void
      {
         if(param4)
         {
            param2.offsetPoint(param4);
         }
         var _loc5_:Rectangle = param1.getRect(param1);
         var _loc6_:Number = param2.width - param1.width;
         var _loc7_:Number = param2.height - param1.height;
         switch(param3)
         {
            case AlignType.TOP_LEFT:
               param1.x = param2.x;
               param1.y = param2.y;
               break;
            case AlignType.TOP_CENTER:
               param1.x = param2.x + _loc6_ / 2 - _loc5_.x;
               param1.y = param2.y;
               break;
            case AlignType.TOP_RIGHT:
               param1.x = param2.x + _loc6_ - _loc5_.x;
               param1.y = param2.y;
               break;
            case AlignType.MIDDLE_LEFT:
               param1.x = param2.x;
               param1.y = param2.y + _loc7_ / 2 - _loc5_.x;
               break;
            case AlignType.MIDDLE_CENTER:
               param1.x = param2.x + _loc6_ / 2 - _loc5_.x;
               param1.y = param2.y + _loc7_ / 2 - _loc5_.y;
               break;
            case AlignType.MIDDLE_RIGHT:
               param1.x = param2.x + _loc6_ - _loc5_.x;
               param1.y = param2.y + _loc7_ / 2 - _loc5_.y;
               break;
            case AlignType.BOTTOM_LEFT:
               param1.x = param2.x;
               param1.y = param2.y + _loc7_ - _loc5_.y;
               break;
            case AlignType.BOTTOM_CENTER:
               param1.x = param2.x + _loc6_ / 2 - _loc5_.x;
               param1.y = param2.y + _loc7_ - _loc5_.y;
               break;
            case AlignType.BOTTOM_RIGHT:
               param1.x = param2.x + _loc6_ - _loc5_.x;
               param1.y = param2.y + _loc7_ - _loc5_.y;
         }
      }
      
      public static function FillColor(param1:DisplayObject, param2:uint) : void
      {
         var _loc3_:ColorTransform = new ColorTransform();
         _loc3_.color = param2;
         param1.transform.colorTransform = _loc3_;
      }
      
      public static function getColor(param1:DisplayObject, param2:uint = 0, param3:uint = 0, param4:Boolean = false) : uint
      {
         var _loc5_:BitmapData = new BitmapData(param1.width,param1.height);
         _loc5_.draw(param1);
         var _loc6_:uint = !param4 ? _loc5_.getPixel(int(param2),int(param3)) : _loc5_.getPixel32(int(param2),int(param3));
         _loc5_.dispose();
         return _loc6_;
      }
      
      public static function uniformScale(param1:DisplayObject, param2:Number) : void
      {
         if(param1.width >= param1.height)
         {
            param1.width = param2;
            param1.scaleY = param1.scaleX;
         }
         else
         {
            param1.height = param2;
            param1.scaleX = param1.scaleY;
         }
      }
      
      public static function copyDisplayAsBmp(param1:DisplayObject, param2:Boolean = true) : Bitmap
      {
         var _loc3_:Number = NaN;
         var _loc4_:Number = NaN;
         _loc4_ = param1.scaleY;
         _loc3_ = param1.scaleX;
         var _loc5_:BitmapData = new BitmapData(param1.width,param1.height,true,16777215);
         var _loc6_:Rectangle = param1.getRect(param1);
         var _loc7_:Matrix = new Matrix();
         if(_loc3_ < 0)
         {
            param1.scaleX = -param1.scaleX;
         }
         if(_loc4_ < 0)
         {
            param1.scaleY = -param1.scaleY;
         }
         _loc7_.createBox(param1.scaleX,param1.scaleY,0,-_loc6_.x * param1.scaleX,-_loc6_.y * param1.scaleY);
         _loc5_.draw(param1,_loc7_);
         param1.scaleX = _loc3_;
         param1.scaleY = _loc4_;
         var _loc8_:Bitmap = new Bitmap(_loc5_,PixelSnapping.AUTO,param2);
         if(_loc3_ < 0)
         {
            _loc8_.scaleX = -1;
         }
         if(_loc4_ < 0)
         {
            _loc8_.scaleY = -1;
         }
         _loc8_.x = _loc6_.x * param1.scaleX;
         _loc8_.y = _loc6_.y * param1.scaleY;
         return _loc8_;
      }
      
      public static function mouseEnabledAll(param1:InteractiveObject, param2:Boolean = false) : void
      {
         var container:DisplayObjectContainer;
         var i:int = 0;
         var child:InteractiveObject = null;
         var target:InteractiveObject = param1;
         var isAll:Boolean = param2;
         var b:Boolean = Boolean(MOUSE_EVENT_LIST.some(function(param1:String, param2:int, param3:Array):Boolean
         {
            if(target.hasEventListener(param1))
            {
               return true;
            }
            return false;
         }));
         if(!b)
         {
            if(target.name.indexOf("instance") != -1)
            {
               target.mouseEnabled = false;
            }
         }
         container = target as DisplayObjectContainer;
         if(container)
         {
            i = container.numChildren - 1;
            while(i >= 0)
            {
               child = container.getChildAt(i) as InteractiveObject;
               if(child)
               {
                  mouseEnabledAll(child);
               }
               i--;
            }
         }
      }
      
      public static function removeDescTxt(param1:DisplayObjectContainer) : void
      {
         var _loc2_:TextField = null;
         var _loc3_:uint = uint(param1.numChildren);
         var _loc4_:uint = 0;
         while(_loc4_ < _loc3_)
         {
            _loc2_ = param1.getChildAt(_loc4_) as TextField;
            if(Boolean(_loc2_) && _loc2_.name == "desc_txt")
            {
               param1.removeChild(_loc2_);
               break;
            }
            _loc4_++;
         }
      }
      
      public static function depthSort(param1:DisplayObjectContainer) : void
      {
         var _loc3_:uint = 0;
         var _loc5_:DisplayObject = null;
         var _loc2_:Array = new Array();
         var _loc4_:uint = uint(param1.numChildren);
         _loc3_ = 0;
         while(_loc3_ < _loc4_)
         {
            _loc2_.push(param1.getChildAt(_loc3_));
            _loc3_++;
         }
         _loc2_.sortOn("y");
         _loc3_ = 0;
         while(_loc3_ < _loc4_)
         {
            _loc5_ = _loc2_[_loc3_];
            if(_loc5_ != param1.getChildAt(_loc3_))
            {
               param1.setChildIndex(_loc5_,_loc3_);
            }
            _loc3_++;
         }
      }
   }
}

