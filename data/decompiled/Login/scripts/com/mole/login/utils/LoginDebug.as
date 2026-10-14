package com.mole.login.utils
{
   import com.mole.login.LoginData;
   import flash.display.Sprite;
   import flash.system.Capabilities;
   import flash.text.TextField;
   
   public class LoginDebug extends Sprite
   {
      
      private static var _inst:LoginDebug;
      
      public static var DEBUG:Boolean = false;
      
      private var _trace_txt:TextField;
      
      public function LoginDebug()
      {
         super();
         this._trace_txt = new TextField();
         this._trace_txt.width = 960;
         this._trace_txt.height = 560;
         addChild(this._trace_txt);
      }
      
      public static function get inst() : LoginDebug
      {
         if(_inst == null)
         {
            _inst = new LoginDebug();
            _inst.mouseChildren = false;
            _inst.mouseEnabled = false;
         }
         return _inst;
      }
      
      public function write(param1:String) : void
      {
         if(DEBUG)
         {
            this._trace_txt.appendText(param1 + "\t登录渠道--->" + LoginData.loginType + "\n");
         }
      }
      
      public function sendError(param1:String, param2:Boolean = false) : void
      {
         if(Boolean(LoginData.userID) || Boolean(LoginData.email) || param2)
         {
            new SendLoginError(param1 + "  LoginType=" + LoginData.loginType + "  OS=" + Capabilities.version + "  Version=" + Capabilities.version);
         }
      }
      
      public function destroy() : void
      {
      }
   }
}

