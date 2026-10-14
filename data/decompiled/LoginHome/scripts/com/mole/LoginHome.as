package com.mole
{
   import com.mole.login.*;
   import com.mole.login.utils.*;
   import flash.display.MovieClip;
   import flash.display.Sprite;
   import flash.events.*;
   
   [SWF(width="960", height="560", backgroundColor="#ffffff", frameRate="24")]
   public class LoginHome extends Sprite
   {
      
      private static var _inst:LoginHome;
      
      public static const ENTER_LOGIN:String = "enterLogin";
      
      public static const START_LOGIN:String = "startLogin";
      
      private var _loading:MovieClip;
      
      private var _home:LoginHomePage;
      
      private var _regUserInfo:Object;
      
      public function LoginHome()
      {
         super();
      }
      
      public static function get inst() : LoginHome
      {
         return _inst;
      }
      
      public function setVersionManager(param1:Object) : void
      {
         VersionManager.setup(param1);
      }
      
      public function init() : void
      {
         _inst = this;
         this._home = new LoginHomePage();
         this._home.addEventListener(START_LOGIN,this.onStartLogin);
         addChild(this._home);
         this._loading = new RES_Login_Loading();
         this._loading.x = 960 / 2;
         this._loading.y = 560 / 2;
         this._loading.visible = false;
         LoginHome.inst.addChild(this._loading);
      }
      
      public function openRegView() : void
      {
         this._regUserInfo = {"openRegsit":true};
         dispatchEvent(new Event(ENTER_LOGIN));
      }
      
      private function regSuccFun(param1:Object) : void
      {
         this._regUserInfo = param1;
         this.destroy();
         dispatchEvent(new Event(ENTER_LOGIN));
      }
      
      private function regFailFun() : void
      {
      }
      
      private function onStartLogin(param1:Event) : void
      {
         this.destroy();
         dispatchEvent(new Event(ENTER_LOGIN));
      }
      
      public function destroy() : void
      {
         _inst = null;
         if(this._home)
         {
            this._home.removeEventListener(START_LOGIN,this.onStartLogin);
            this._home.destroy();
            this._home = null;
         }
         DisplayUtil.removeForParent(this);
      }
      
      public function showLoading() : void
      {
         this._loading.visible = true;
         addChild(this._loading);
      }
      
      public function hideLoading() : void
      {
         this._loading.visible = false;
      }
      
      public function get regUserInfo() : Object
      {
         return this._regUserInfo;
      }
      
      public function set regUserInfo(param1:Object) : void
      {
         this._regUserInfo = param1;
      }
   }
}

