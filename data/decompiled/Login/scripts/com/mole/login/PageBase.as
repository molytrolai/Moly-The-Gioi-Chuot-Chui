package com.mole.login
{
   import com.mole.login.utils.AlignType;
   import com.mole.login.utils.DisplayUtil;
   import flash.display.Sprite;
   import flash.geom.Rectangle;
   
   public class PageBase extends Sprite
   {
      
      protected var _initData:Object;
      
      protected var _page_mc:Sprite;
      
      public function PageBase(param1:Sprite)
      {
         super();
         this._page_mc = param1;
         DisplayUtil.align(this._page_mc,new Rectangle(0,0,960,560),AlignType.MIDDLE_CENTER);
         addChild(this._page_mc);
      }
      
      public function init(param1:Object) : void
      {
         this._initData = param1;
      }
      
      public function destroy() : void
      {
         DisplayUtil.removeForParent(this);
      }
   }
}

