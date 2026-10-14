package com.mole
{
   import com.mole.login.*;
   import com.mole.login.net.*;
   import com.mole.login.utils.*;
   import flash.display.MovieClip;
   import flash.display.Sprite;
   import flash.events.*;
   import flash.external.*;
   import flash.net.*;
   import flash.ui.*;
   
   [SWF(width="960", height="560", backgroundColor="#ffffff", frameRate="24")]
   public class Login extends Sprite
   {
      
      private static var _inst:Login;
      
      public static const REGIST:String = "regist";
      
      private var _config:LoginServerConfig;
      
      private var _page:PageBase;
      
      private var _loginSocket:LoginSocket;
      
      private var _registPanel:LoginRegister;
      
      private var _loading:MovieClip;
      
      private var _cmdMsg:String = "";
      
      private var _regUserInfo:Object;
      
      private var _isCheckUid:Boolean = false;
      
      public function Login()
      {
         super();
         _inst = this;
         this._loading = new RES_Login_Loading();
         this._loading.x = 960 / 2;
         this._loading.y = 560 / 2;
         if(ExternalInterface.available)
         {
            LoginData.loginType = 0;
            LoginData.adMsg = ExternalInterface.call("getAd");
         }
         else
         {
            LoginData.loginType = 0;
         }
         this._config = LoginServerConfig.inst;
         if(stage)
         {
            this.onAddedToStage();
         }
         else
         {
            addEventListener(Event.ADDED_TO_STAGE,this.onAddedToStage);
         }
      }
      
      public static function get inst() : Login
      {
         return _inst;
      }
      
      private function onAddedToStage(param1:Event = null) : void
      {
         stage.addEventListener(KeyboardEvent.KEY_DOWN,this.onKeyDownHd);
         addEventListener(Event.REMOVED_FROM_STAGE,this.onRemoveFromStage);
      }
      
      private function onRemoveFromStage(param1:Event) : void
      {
         removeEventListener(Event.REMOVED_FROM_STAGE,this.onRemoveFromStage);
         stage.removeEventListener(KeyboardEvent.KEY_DOWN,this.onKeyDownHd);
      }
      
      private function onKeyDownHd(param1:KeyboardEvent) : void
      {
         var _loc2_:String = null;
         if(param1.keyCode == Keyboard.ENTER)
         {
            if(this._cmdMsg == "openDebug")
            {
               LoginDebug.DEBUG = true;
            }
            this._cmdMsg = "";
         }
         else if(param1.charCode)
         {
            _loc2_ = String.fromCharCode(param1.charCode);
            this._cmdMsg += _loc2_;
         }
      }
      
      public function setVersionManager(param1:Object) : void
      {
         VersionManager.setup(param1);
      }
      
      public function init(param1:XML, param2:Object) : void
      {
         LoginShared.setup();
         this._config.initServerXml(param1);
         this._regUserInfo = param2;
         this.enterPage();
         addChild(this._loading);
         var _loc3_:URLLoader = new URLLoader();
         _loc3_.addEventListener(Event.COMPLETE,this.onGetIpPort);
         _loc3_.addEventListener(IOErrorEvent.IO_ERROR,this.onGetIpPort);
         _loc3_.addEventListener(SecurityErrorEvent.SECURITY_ERROR,this.onGetIpPort);
         var _loc4_:String = "http://" + this._config.moleServerConfig.moleUrl + "/ip.txt";
         _loc3_.load(new URLRequest(_loc4_));
         this._loginSocket = LoginSocket.instance;
      }
      
      public function regLogin(param1:Object) : void
      {
         param1.type = 2;
         this.showPage(2,param1);
      }
      
      private function enterPage() : void
      {
         var _loc1_:Object = null;
         var _loc2_:Array = null;
         if(this._regUserInfo)
         {
            if(this._regUserInfo.openRegsit)
            {
               this.openRegist();
            }
            else
            {
               this.regLogin(this._regUserInfo);
            }
         }
         else
         {
            _loc1_ = LoginUtil.loginSession;
            if(Boolean(_loc1_))
            {
               this.showPage(2);
            }
            else
            {
               _loc2_ = LoginShared.loginList;
               if(Boolean(_loc2_) && _loc2_.length > 0)
               {
                  this.showPage(1);
               }
               else
               {
                  this.showPage(2);
               }
            }
         }
      }
      
      private function onGetIpPort(param1:Event) : void
      {
         var _loc2_:String = null;
         var _loc3_:Array = null;
         DisplayUtil.removeForParent(this._loading);
         this.removeUrlEvent(param1.currentTarget as URLLoader);
         if(param1.type == Event.COMPLETE)
         {
            _loc2_ = String(param1.currentTarget.data);
            _loc3_ = _loc2_.split(":");
            if(_loc3_.length == 2)
            {
               this._loginSocket.setHostPort(_loc3_[0],uint(_loc3_[1]));
            }
            else
            {
               this._loginSocket.setHostPort(this._config.idIP.ip,this._config.idIP.port);
               LoginDebug.inst.sendError("Domain name for IP from mistakes\tIP:" + _loc2_);
            }
         }
         else
         {
            this._loginSocket.setHostPort(this._config.idIP.ip,this._config.idIP.port);
            if(param1.type == IOErrorEvent.IO_ERROR)
            {
               LoginDebug.inst.sendError("[S2: IO ip.txt] Svr=login.mole.61.com:80 E=IO错误具体原因",true);
            }
            else
            {
               LoginDebug.inst.sendError("[S1: HTTP SB ip.txt] Svr=login.mole.61.com:80 E=安全沙箱错误具体原因",true);
            }
         }
      }
      
      private function removeUrlEvent(param1:URLLoader) : void
      {
         param1.removeEventListener(Event.COMPLETE,this.onGetIpPort);
         param1.removeEventListener(IOErrorEvent.IO_ERROR,this.onGetIpPort);
         param1.removeEventListener(SecurityErrorEvent.SECURITY_ERROR,this.onGetIpPort);
      }
      
      public function showPage(param1:uint, param2:Object = null) : void
      {
         var _loc3_:* = undefined;
         if(this._page)
         {
            this._page.destroy();
            this._page = null;
         }
         if(Boolean(param2 == null) && Boolean(ExternalInterface.available) && this._isCheckUid == false)
         {
            _loc3_ = ExternalInterface.call("get_uid");
            if(_loc3_)
            {
               param2 = new Object();
               param2.type = 2;
               param2.uisID = _loc3_;
               param1 = 2;
            }
            this._isCheckUid = true;
         }
         switch(param1)
         {
            case 1:
               this._page = new LoginSelectPage();
               break;
            case 2:
               this._page = new LoginOnePage();
               break;
            case 3:
               this._page = new LoginServerPage();
         }
         this._page.init(param2);
         this._page.addEventListener(REGIST,this.openRegist);
         addChild(this._page);
         addChild(LoginDebug.inst);
      }
      
      private function openRegist(param1:Event = null) : void
      {
         this._registPanel = new LoginRegister();
         this._registPanel.tad = LoginData.adMsg;
         this._registPanel.registerService = "http://account-httpd.61.com/index.php";
         addChild(this._registPanel);
      }
      
      public function enterGame() : void
      {
         dispatchEvent(new Event("loginSucc"));
         this.destroy();
      }
      
      public function get loginData() : Object
      {
         var _loc1_:Object = new Object();
         _loc1_.serNameDict = this._config.nameDict;
         _loc1_.ip = LoginData.ip;
         _loc1_.port = LoginData.port;
         _loc1_.userID = LoginData.userID;
         _loc1_.session = LoginData.session;
         _loc1_.serverID = LoginData.serverID;
         _loc1_.serverList = LoginData.serverList;
         _loc1_.type = LoginData.loginType;
         _loc1_.adByte = LoginData.getAdByte();
         return _loc1_;
      }
      
      public function getAccountState(param1:String) : uint
      {
         var _loc2_:RegExp = /^[0-9]{1,10}$/;
         var _loc3_:RegExp = /\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/;
         var _loc4_:RegExp = /^[a-zA-Z0-9_]{3,20}$/;
         var _loc5_:RegExp = /^[0-9]{11}$/;
         if(_loc2_.test(param1) == true)
         {
            return 1;
         }
         if(_loc3_.test(param1) == true || _loc4_.test(param1) == true || _loc5_.test(param1) == true)
         {
            return 2;
         }
         return 0;
      }
      
      public function destroy() : void
      {
         this._loginSocket.destroy();
         _inst = null;
         this._page.destroy();
         DisplayUtil.removeForParent(this);
      }
   }
}

