package com.mole.login
{
   import com.mole.*;
   import com.mole.login.info.*;
   import com.mole.login.net.*;
   import com.mole.login.type.*;
   import com.mole.login.utils.*;
   import flash.display.SimpleButton;
   import flash.display.Sprite;
   import flash.events.*;
   import flash.filters.*;
   import flash.net.*;
   import flash.text.TextField;
   import flash.ui.*;
   
   public class LoginOnePage extends PageBase
   {
      
      private static var _inst:LoginOnePage;
      
      private var _id_mc:Sprite;
      
      private var _pwd_mc:Sprite;
      
      private var _authCode:LoginOneAuthCode;
      
      private var _rem_id:LoginCheckBox;
      
      private var _rem_pwd:LoginCheckBox;
      
      private var _login_btn:SimpleButton;
      
      private var _findPwd_btn:SimpleButton;
      
      private var _modifyPwd_btn:SimpleButton;
      
      private var _protectPwd_btn:SimpleButton;
      
      private var _reg_btn:SimpleButton;
      
      private var _change_btn:SimpleButton;
      
      private var _id_txt:TextField;
      
      public function LoginOnePage()
      {
         var _loc1_:ColorMatrix = null;
         super(new RES_Login_InfoPanel());
         _inst = this;
         _page_mc.x = _page_mc.y = 0;
         this._id_mc = _page_mc["id_mc"];
         this._pwd_mc = _page_mc["pwd_mc"];
         this._authCode = new LoginOneAuthCode(_page_mc["authCode_mc"]);
         this._rem_id = new LoginCheckBox(_page_mc["rem_id"]);
         this._rem_pwd = new LoginCheckBox(_page_mc["rem_pwd"]);
         this._login_btn = _page_mc["login_btn"];
         this._findPwd_btn = _page_mc["findPwd_btn"];
         this._modifyPwd_btn = _page_mc["modifyPwd_btn"];
         this._protectPwd_btn = _page_mc["protectPwd_btn"];
         this._reg_btn = _page_mc["reg_btn"];
         this._change_btn = _page_mc["systermID"];
         this._login_btn.addEventListener(MouseEvent.CLICK,this.onLogin);
         this._findPwd_btn.addEventListener(MouseEvent.CLICK,this.onFindPwd);
         this._modifyPwd_btn.addEventListener(MouseEvent.CLICK,this.onModifyPwd);
         this._protectPwd_btn.addEventListener(MouseEvent.CLICK,this.onProtectPwd);
         this._reg_btn.addEventListener(MouseEvent.CLICK,this.onOpenReg);
         if(LoginShared.loginList)
         {
            this._change_btn.addEventListener(MouseEvent.CLICK,this.onChange);
         }
         else
         {
            _loc1_ = new ColorMatrix();
            _loc1_.adjustSaturation(-255);
            this._change_btn.filters = [new ColorMatrixFilter(_loc1_)];
            this._change_btn.mouseEnabled = false;
         }
         this._id_txt = this._id_mc["id_txt"];
         this._id_txt.tabEnabled = true;
         this._id_txt.tabIndex = 1;
         this._id_txt.addEventListener(KeyboardEvent.KEY_DOWN,this.onIDKeyDown);
         this._pwd_mc["pwd_txt"].tabEnabled = true;
         this._pwd_mc["pwd_txt"].tabIndex = 2;
         this._pwd_mc["pwd_txt"].displayAsPassword = true;
         this._pwd_mc["pwd_txt"].addEventListener(KeyboardEvent.KEY_DOWN,this.onPwdKeyDown);
         this._rem_id.addEventListener(LoginCheckBox.STATE_CHANGE,this.onRemID);
         this._rem_pwd.addEventListener(LoginCheckBox.STATE_CHANGE,this.onRemPwd);
         LoginSocket.addCmdListener(LoginCmd.CMD_LOGIN,this.onSocketLogin);
         this.setAuthCode(false);
      }
      
      public static function get inst() : LoginOnePage
      {
         return _inst;
      }
      
      public function setAuthCode(param1:Boolean) : void
      {
         if(param1)
         {
            this._id_mc.y = 173;
            this._pwd_mc.y = 206;
            _page_mc["rem_id"].y = 173;
            _page_mc["rem_pwd"].y = 206;
         }
         else
         {
            this._id_mc.y = 182;
            this._pwd_mc.y = 222;
            _page_mc["rem_id"].y = 182;
            _page_mc["rem_pwd"].y = 222;
         }
      }
      
      private function onInitView(param1:Event) : void
      {
         this.stage.focus = this._id_txt;
      }
      
      private function onIDKeyDown(param1:KeyboardEvent) : void
      {
         if(param1.keyCode == Keyboard.ENTER)
         {
            this.stage.focus = this._pwd_mc["pwd_txt"];
         }
      }
      
      private function onPwdKeyDown(param1:KeyboardEvent) : void
      {
         if(param1.keyCode == Keyboard.ENTER)
         {
            this.checkLogin();
         }
      }
      
      private function onSocketLogin(param1:EventTaomee) : void
      {
         var _loc3_:String = null;
         var _loc4_:RegCipher = null;
         var _loc2_:LoginProtocol = param1.EventObj as LoginProtocol;
         if(_loc2_.flag == 0)
         {
            _loc3_ = this._pwd_mc["pwd_txt"].text;
            _loc4_ = new RegCipher();
            if(_loc4_.check(_loc3_))
            {
               LoginAlert.show(LoginAlert.NORMAL_WARN,"你的密码太简单啦！英文+数字更加安全哦！",LoginAlert.MODIFY_PWD_AN | LoginAlert.ENTER_GAME_AN,[this.modifyPwd,this.enterGameConfrim],[[],[]]);
            }
            else
            {
               this.enterGameConfrim();
            }
            this.checkUserShared(_loc3_);
         }
         else
         {
            if(_loc2_.flag == 1)
            {
               LoginAlert.show(LoginAlert.SYS_ERROR,"密码错误！",LoginAlert.GOT_AN);
            }
            else if(_loc2_.flag == 2)
            {
               LoginAlert.show(LoginAlert.SYS_ERROR,"验证码错误！",LoginAlert.GOT_AN);
            }
            this._authCode.show(_loc2_.codeID,_loc2_.picLoader);
         }
      }
      
      private function checkUserShared(param1:String) : void
      {
         var _loc2_:Object = null;
         if(this._rem_id.selected)
         {
            _loc2_ = new Object();
            _loc2_.remID = this._rem_id.selected;
            _loc2_.userID = LoginData.userID;
            _loc2_.userCode = this._id_txt.text;
            if(this._rem_pwd.selected)
            {
               if(param1.length != 32)
               {
                  param1 = LoginUtil.upsetPwd(this._pwd_mc["pwd_txt"].text);
               }
               _loc2_.pwd = param1;
            }
            _loc2_.remPwd = this._rem_pwd.selected;
            _loc2_.time = new Date().time;
            LoginShared.addUser(_loc2_);
         }
         else
         {
            LoginShared.removeUser(LoginData.userID);
         }
      }
      
      private function enterGameConfrim() : void
      {
         Login.inst.showPage(3);
      }
      
      private function onRemID(param1:EventTaomee) : void
      {
         if(param1.EventObj == false)
         {
            this._rem_pwd.selected = false;
         }
      }
      
      private function onRemPwd(param1:EventTaomee) : void
      {
         StatisticsManager.send(461);
         if(param1.EventObj)
         {
            LoginAlert.show(LoginAlert.NORMAL_WARN,"只有在自己家里上网才能选择，并要牢记帐号和密码哦！",LoginAlert.GOT_AN);
            this._rem_id.selected = true;
         }
      }
      
      override public function init(param1:Object) : void
      {
         var _loc2_:Object = null;
         var _loc3_:Object = null;
         super.init(param1);
         this._rem_id.setState(false);
         this._rem_pwd.setState(false);
         if(_initData)
         {
            if(_initData.type == 2)
            {
               this._rem_id.setState(true);
               this._id_txt.text = _initData.uisID;
               _loc2_ = new Object();
               _loc2_.userID = _initData.uisID;
            }
            else
            {
               if(_initData.userID)
               {
                  this._id_txt.text = _initData.userID;
                  LoginPktParser.GetAuthCode();
               }
               if(Boolean(_initData.remPwd) && Boolean(_initData.pwd))
               {
                  this._pwd_mc["pwd_txt"].text = _initData.pwd;
               }
               else
               {
                  this._pwd_mc["pwd_txt"].text = "";
               }
               this._rem_id.setState(_initData.remID);
               this._rem_pwd.setState(_initData.remPwd);
               if(_initData.autoLogin)
               {
                  this.onLogin();
               }
            }
         }
         else
         {
            this._rem_id.setState(true);
            _loc3_ = LoginUtil.loginSession;
            if(_loc3_)
            {
               this._id_txt.text = String(_loc3_.userID);
               this._pwd_mc["pwd_txt"].text = "********";
               LoginData.session = _loc3_.session;
            }
            else
            {
               this._id_txt.text = "";
               this._pwd_mc["pwd_txt"].text = "";
               if(this.stage)
               {
                  this.onInitView(null);
               }
               else
               {
                  addEventListener(Event.ADDED_TO_STAGE,this.onInitView);
               }
            }
         }
      }
      
      private function onLogin(param1:MouseEvent = null) : void
      {
         var _loc3_:String = null;
         var _loc2_:Object = LoginUtil.loginSession;
         if(Boolean(_loc2_) && _loc2_.userID == uint(this._id_txt.text))
         {
            LoginData.userID = _loc2_.userID;
            LoginDebug.inst.write("UserID---->" + LoginData.userID);
            this.enterGameConfrim();
            _loc3_ = this._pwd_mc["pwd_txt"].text;
            this.checkUserShared(_loc3_);
         }
         else
         {
            this.checkLogin();
         }
      }
      
      private function checkLogin() : void
      {
         var _loc1_:String = this._id_txt.text;
         var _loc2_:String = this._pwd_mc["pwd_txt"].text;
         if(Login.inst.getAccountState(_loc1_) > 0)
         {
            if(Boolean(_loc2_) && _loc2_.length >= 6)
            {
               this.sendLogin(_loc1_,_loc2_);
            }
            else
            {
               LoginAlert.show(LoginAlert.SYS_PROMPT,"密码不能为空且要大于5位！",LoginAlert.GOT_AN);
            }
         }
         else
         {
            LoginAlert.show(LoginAlert.SYS_PROMPT,"帐号错误。",LoginAlert.GOT_AN);
         }
      }
      
      private function modifyPwd() : void
      {
         navigateToURL(new URLRequest("http://account.61.com/main?goto_url=%2Fchange&referer=%2Fchange"));
      }
      
      private function sendLogin(param1:String, param2:String) : void
      {
         if(param2.length == 32)
         {
            param2 = LoginUtil.changeRemenberedPwdPos(param2);
         }
         this.checkUserShared(param2);
         if(Login.inst.getAccountState(param1) == 1)
         {
            LoginPktParser.IdLogin(uint(param1),param2,this._authCode.authObj);
         }
         else
         {
            LoginPktParser.EmailLogin(param1,param2,this._authCode.authObj);
         }
         TongjiUtil.sendTongji(2,param1);
      }
      
      private function onFindPwd(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("http://account.61.com/forget"));
      }
      
      private function onModifyPwd(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("https://account.61.com"));
      }
      
      private function onProtectPwd(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("https://account.61.com"));
      }
      
      private function onChange(param1:MouseEvent) : void
      {
         Login.inst.showPage(1);
      }
      
      private function onOpenReg(param1:MouseEvent) : void
      {
         StatisticsManager.send(455);
         navigateToURL(new URLRequest("https://account.61.com/register"));
      }
      
      private function regSuccFun(param1:Object) : void
      {
         this._rem_id.setState(true);
         this._id_txt.text = param1.uisID;
      }
      
      private function regFailFun() : void
      {
      }
      
      override public function destroy() : void
      {
         removeEventListener(Event.ADDED_TO_STAGE,this.onInitView);
         this._pwd_mc["pwd_txt"].removeEventListener(KeyboardEvent.KEY_DOWN,this.onPwdKeyDown);
         this._id_txt.removeEventListener(KeyboardEvent.KEY_DOWN,this.onIDKeyDown);
         LoginSocket.removeCmdListener(LoginCmd.CMD_LOGIN,this.onSocketLogin);
         this._authCode.destroy();
         this._rem_id.removeEventListener(LoginCheckBox.STATE_CHANGE,this.onRemID);
         this._rem_pwd.removeEventListener(LoginCheckBox.STATE_CHANGE,this.onRemPwd);
         this._login_btn.removeEventListener(MouseEvent.CLICK,this.onLogin);
         this._findPwd_btn.removeEventListener(MouseEvent.CLICK,this.onFindPwd);
         this._modifyPwd_btn.removeEventListener(MouseEvent.CLICK,this.onModifyPwd);
         this._protectPwd_btn.removeEventListener(MouseEvent.CLICK,this.onProtectPwd);
         this._reg_btn.removeEventListener(MouseEvent.CLICK,this.onOpenReg);
         super.destroy();
      }
   }
}

