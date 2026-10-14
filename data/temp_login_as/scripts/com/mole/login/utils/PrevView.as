package com.mole.login.utils
{
   import flash.display.*;
   import flash.events.*;
   import flash.geom.*;
   import flash.net.*;
   
   public class PrevView
   {
      
      private var _clothsArray:Array;
      
      private var _levelCon:RoleViewLevel;
      
      private var _roleType:uint;
      
      private var _loaderHash:HashMap;
      
      public function PrevView(param1:Sprite)
      {
         super();
         this._levelCon = new RoleViewLevel(param1);
         this._loaderHash = new HashMap();
      }
      
      public function setRoleType(param1:uint) : void
      {
         this._roleType = param1;
      }
      
      public function setCloths(param1:Array) : void
      {
         this._clothsArray = param1;
         if(this._roleType != 0)
         {
            while(this._levelCon.body_mc.numChildren > 1)
            {
               this._levelCon.body_mc.removeChildAt(0);
            }
            this.loadCloth(this._roleType,1);
            this.loadCloth(this._roleType + 100,2);
            this._levelCon.body_mc.x -= 20;
            this._levelCon.body_mc.y += 20;
         }
         this.showCloths();
      }
      
      private function showCloths() : void
      {
         var _loc1_:Object = null;
         var _loc2_:Sprite = null;
         var _loc3_:Loader = null;
         this._clothsArray.sortOn("layer",Array.NUMERIC);
         var _loc4_:uint = 0;
         while(_loc4_ < this._clothsArray.length)
         {
            _loc1_ = this._clothsArray[_loc4_];
            if(Boolean(_loc1_ && _loc1_.id != 0 && _loc1_.layer != 0) && Boolean(_loc1_.layer != 1) && _loc1_.layer != 88)
            {
               this.loadCloth(_loc1_.id,_loc1_.layer);
            }
            _loc4_++;
         }
      }
      
      private function loadCloth(param1:uint, param2:uint) : void
      {
         var _loc3_:Sprite = null;
         var _loc4_:Loader = null;
         _loc4_ = new Loader();
         _loc4_.load(new URLRequest("resource/cloth/prevIcon/" + param1 + ".swf"));
         _loc4_.contentLoaderInfo.addEventListener(Event.COMPLETE,this.onLoaderClothComplete);
         _loc4_.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR,this.onLoaderClothError);
         _loc3_ = new Sprite();
         _loc3_.name = "name" + param1;
         if(param2 != 0)
         {
            this._loaderHash.add(_loc4_,_loc3_);
            this._levelCon.clothsCon.addChild(_loc3_);
         }
      }
      
      private function onLoaderClothError(param1:IOErrorEvent) : void
      {
      }
      
      public function setColor(param1:*) : void
      {
         var _loc2_:Array = null;
         var _loc5_:Sprite = null;
         var _loc6_:Object = null;
         if(this._roleType != 0)
         {
            return;
         }
         if(param1 as String)
         {
            _loc2_ = this.getPrimitiveColors(param1);
         }
         else if(!isNaN(param1))
         {
            _loc2_ = this.getPrimitiveColors(param1.toString(16));
         }
         var _loc3_:uint = 1;
         var _loc4_:Sprite = this._levelCon.body_mc;
         while(true)
         {
            _loc5_ = _loc4_["pv_color" + _loc3_];
            if(!_loc5_)
            {
               break;
            }
            _loc6_ = {
               "red":_loc2_[0],
               "green":_loc2_[1],
               "blue":_loc2_[2]
            };
            _loc5_["pv_color"].transform.colorTransform = new ColorTransform(_loc6_.red / 256,_loc6_.green / 256,_loc6_.blue / 256,1);
            _loc3_++;
         }
      }
      
      private function getPrimitiveColors(param1:String) : Array
      {
         var _loc6_:String = null;
         var _loc7_:String = null;
         var _loc8_:String = null;
         var _loc2_:Object = {
            0:0,
            1:1,
            2:2,
            3:3,
            4:4,
            5:5,
            6:6,
            7:7,
            8:8,
            9:9,
            "a":10,
            "b":11,
            "c":12,
            "d":13,
            "e":14,
            "f":15
         };
         var _loc3_:String = param1;
         if(_loc3_.indexOf("#") > -1)
         {
            _loc3_ = _loc3_.slice(1);
         }
         while(_loc3_.length < 6)
         {
            _loc3_ = "0" + _loc3_;
         }
         _loc3_ = _loc3_.toLocaleLowerCase();
         var _loc4_:Array = [];
         var _loc5_:uint = 0;
         while(_loc5_ < 6)
         {
            _loc6_ = _loc3_.substr(_loc5_,2);
            _loc7_ = _loc6_.substr(0,1);
            _loc8_ = _loc6_.substr(1,1);
            _loc4_.push(_loc2_[_loc7_] * 16 + _loc2_[_loc8_]);
            _loc5_ += 2;
         }
         return _loc4_;
      }
      
      private function onLoaderClothComplete(param1:Event) : void
      {
         var _loc2_:LoaderInfo = param1.currentTarget as LoaderInfo;
         _loc2_.removeEventListener(Event.COMPLETE,this.onLoaderClothComplete);
         var _loc3_:Loader = _loc2_.loader;
         var _loc4_:Sprite = this._loaderHash.getValue(_loc3_);
         var _loc5_:MovieClip = _loc2_.content as MovieClip;
         var _loc6_:DisplayObject = _loc5_.getChildAt(0);
         if(_loc6_)
         {
            _loc6_.x = _loc6_.y = 0;
         }
         _loc4_.addChild(_loc6_);
      }
   }
}

