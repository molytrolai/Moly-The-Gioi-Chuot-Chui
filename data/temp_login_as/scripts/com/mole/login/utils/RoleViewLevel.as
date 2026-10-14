package com.mole.login.utils
{
   import flash.display.*;
   
   public class RoleViewLevel extends Sprite
   {
      
      private var _body_mc:Sprite;
      
      private var _clothsCon:Sprite;
      
      private var _bgCon:Sprite;
      
      public function RoleViewLevel(param1:Sprite)
      {
         super();
         param1.addChild(this);
         this._body_mc = param1["body_mc"];
         this._clothsCon = new Sprite();
         this._body_mc.addChild(this._clothsCon);
      }
      
      public function get body_mc() : Sprite
      {
         return this._body_mc;
      }
      
      public function get clothsCon() : Sprite
      {
         return this._clothsCon;
      }
   }
}

