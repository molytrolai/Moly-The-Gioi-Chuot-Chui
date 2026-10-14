package com.mole
{
   import com.mole.login.utils.*;
   import flash.display.MovieClip;
   import flash.display.SimpleButton;
   import flash.display.Sprite;
   import flash.events.*;
   import flash.net.*;
   import flash.text.TextField;
   import flash.utils.ByteArray;
   import org.taomee.register.*;
   import org.taomee.register.event.*;
   import org.taomee.register.util.*;
   
   public class LoginRegister extends Sprite
   {
      
      private var _mainUI:UI_Register_panel;
      
      private var _passwordTxt:TextField;
      
      private var _repatePasswordTxt:TextField;
      
      private var _authCodeTxt:TextField;
      
      private var _changeCaptchaBtn:SimpleButton;
      
      private var _registerBtn:SimpleButton;
      
      private var _passWordErrorTxt:TextField;
      
      private var _repatePasswordErrorTxt:TextField;
      
      private var _authCodeErrorTxt:TextField;
      
      private var _captchaComp:CaptchaComponent;
      
      private var _alertPanel:AlertPanel;
      
      private var _mimiNum:int;
      
      private var _passWord:String;
      
      private var _closeBtn:SimpleButton;
      
      private var _registerSuccessPanel:RegisterSuccessPanel;
      
      private var _registerService:String;
      
      private var _tad:String = "gf";
      
      private var _comboxMC:MovieClip;
      
      private var _serviceBtn:SimpleButton;
      
      private var _agreeTxt:TextField;
      
      private var flie:FileReference = new FileReference();
      
      private var file:FileReference;
      
      public function LoginRegister()
      {
         super();
         this._mainUI = new UI_Register_panel();
         this._closeBtn = this._mainUI.closeBtn;
         this._closeBtn.tabEnabled = false;
         addChild(this._mainUI);
         this.initView();
         this.initEvent();
         this._mainUI.x = (960 - this._mainUI.width) / 2;
         this._mainUI.y = (560 - this._mainUI.height) / 2 - 55;
      }
      
      public function set tad(param1:String) : void
      {
         this._tad = param1;
      }
      
      public function set registerService(param1:String) : void
      {
         this._registerService = param1;
         RegisterControl.instance.setup(1,this._registerService,this._tad);
      }
      
      private function initView() : void
      {
         this._passwordTxt = this._mainUI.passwordTxt;
         this._passwordTxt.displayAsPassword = true;
         this._passwordTxt.tabIndex = 1;
         this._repatePasswordTxt = this._mainUI.repatePasswordTxt;
         this._repatePasswordTxt.displayAsPassword = true;
         this._repatePasswordTxt.tabIndex = 2;
         this._authCodeTxt = this._mainUI.authCodeTxt;
         this._authCodeTxt.restrict = "0-9";
         this._authCodeTxt.tabIndex = 3;
         this._changeCaptchaBtn = this._mainUI.changeCaptchaBtn;
         this._changeCaptchaBtn.tabEnabled = false;
         this._registerBtn = this._mainUI.registerBtn;
         this._passWordErrorTxt = this._mainUI.passWordErrorTxt;
         this._passWordErrorTxt.mouseEnabled = false;
         this._passWordErrorTxt.tabEnabled = false;
         this._repatePasswordErrorTxt = this._mainUI.repatePasswordErrorTxt;
         this._repatePasswordErrorTxt.mouseEnabled = false;
         this._repatePasswordErrorTxt.tabEnabled = false;
         this._authCodeErrorTxt = this._mainUI.authCodeErrorTxt;
         this._authCodeErrorTxt.mouseEnabled = false;
         this._authCodeErrorTxt.tabEnabled = false;
         this._captchaComp = new CaptchaComponent();
         this._captchaComp.tabEnabled = false;
         this._captchaComp.scaleX = this._captchaComp.scaleY = 0.9;
         this._captchaComp.x = 278;
         this._captchaComp.y = 136;
         this._mainUI.addChild(this._captchaComp);
         this._alertPanel = new AlertPanel();
         this._alertPanel.x = (960 - this._alertPanel.width) / 2;
         this._alertPanel.y = (560 - this._alertPanel.height) / 2 - 55;
         this._comboxMC = this._mainUI.comboxMC;
         this._serviceBtn = this._mainUI.serviceBtn;
         this._agreeTxt = this._mainUI.agreeTxt;
      }
      
      private function initEvent() : void
      {
         this._registerBtn.addEventListener(MouseEvent.CLICK,this.onRegisterBtnClick);
         this._changeCaptchaBtn.addEventListener(MouseEvent.CLICK,this.onChageCaptchaBtnClick);
         this._closeBtn.addEventListener(MouseEvent.CLICK,this.onClose);
         addEventListener(Event.ADDED_TO_STAGE,this.onAddToStage);
         this._passwordTxt.addEventListener(FocusEvent.FOCUS_OUT,this.onPasswordFocusOut);
         this._repatePasswordTxt.addEventListener(FocusEvent.FOCUS_OUT,this.onRepatePasswordFocusOut);
         this._comboxMC.addEventListener(MouseEvent.CLICK,this.onCommboxClick);
         this._serviceBtn.addEventListener(MouseEvent.CLICK,this.onServiceClick);
         RegisterControl.instance.addEventListener(CaptchaEvent.REGISTER_CAPTCHA_RECEIVED,this.onCaptchaReceived);
      }
      
      private function onCaptchaReceived(param1:CaptchaEvent) : void
      {
         this._changeCaptchaBtn.mouseEnabled = true;
      }
      
      private function onCommboxClick(param1:MouseEvent) : void
      {
         var _loc2_:int = this._comboxMC.currentFrame == 1 ? 2 : 1;
         this._comboxMC.gotoAndStop(_loc2_);
      }
      
      private function onServiceClick(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("http://www.61.com/about/service.html"),"_blank");
      }
      
      private function removeEvent() : void
      {
         this._registerBtn.removeEventListener(MouseEvent.CLICK,this.onRegisterBtnClick);
         this._changeCaptchaBtn.removeEventListener(MouseEvent.CLICK,this.onChageCaptchaBtnClick);
         this._closeBtn.removeEventListener(MouseEvent.CLICK,this.onClose);
         removeEventListener(Event.ADDED_TO_STAGE,this.onAddToStage);
         this._passwordTxt.removeEventListener(FocusEvent.FOCUS_OUT,this.onPasswordFocusOut);
         this._repatePasswordTxt.removeEventListener(FocusEvent.FOCUS_OUT,this.onRepatePasswordFocusOut);
         this._serviceBtn.removeEventListener(MouseEvent.CLICK,this.onServiceClick);
      }
      
      private function onRepatePasswordFocusOut(param1:FocusEvent) : void
      {
         this.checkRepatePassword();
      }
      
      private function checkRepatePassword() : Boolean
      {
         var _loc1_:String = this._passwordTxt.text;
         var _loc2_:String = this._repatePasswordTxt.text;
         if(_loc2_ != _loc1_)
         {
            this._repatePasswordErrorTxt.text = "*2次输入密码不一致";
            return false;
         }
         this._repatePasswordErrorTxt.text = "";
         return true;
      }
      
      private function onPasswordFocusOut(param1:FocusEvent) : void
      {
         this.checkPassword(this._passwordTxt.text);
      }
      
      private function onAddToStage(param1:Event) : void
      {
         if(this._captchaComp)
         {
            this._captchaComp.refreshCaptcha();
            stage.focus = this._passwordTxt;
         }
      }
      
      private function onClose(param1:MouseEvent) : void
      {
         this.destory();
         var _loc2_:Array = LoginShared.loginList;
         Login.inst.showPage(2);
      }
      
      private function checkPassword(param1:String) : Boolean
      {
         if(param1 == null || param1 == "")
         {
            this._passWordErrorTxt.text = "*密码不可以为空";
            return false;
         }
         if(param1.length < 6 || param1.length > 16)
         {
            this._passWordErrorTxt.text = "*密码过短，请输入6到16个字符的密码";
            return false;
         }
         if(WeakPasswordUtil.isWeakPassword(param1))
         {
            this._passWordErrorTxt.text = "密码太简单,请尝试数字,字母和下划线的组合";
            return false;
         }
         this._passWordErrorTxt.text = "";
         return true;
      }
      
      private function onRegisterBtnClick(param1:MouseEvent) : void
      {
         var _loc2_:String = this._passwordTxt.text;
         if(!this.checkPassword(_loc2_))
         {
            return;
         }
         if(!this.checkRepatePassword())
         {
            return;
         }
         var _loc3_:String = this._authCodeTxt.text;
         if(_loc3_ == null || _loc3_ == "")
         {
            this._authCodeErrorTxt.text = "*请输入验证码";
            return;
         }
         this._authCodeErrorTxt.text = "";
         if(this._comboxMC.currentFrame != 1)
         {
            this._agreeTxt.text = "你还没有同意注册协议.";
            return;
         }
         this._agreeTxt.text = "";
         if(!this._captchaComp.mouseEnabled)
         {
            return;
         }
         this._registerBtn.mouseEnabled = false;
         RegisterControl.instance.addEventListener(RegisterSuccessEvent.REGISTER_SUCCESS,this.onRegisterReturn);
         RegisterControl.instance.addEventListener(RegisterFailEvent.REGISTER_FAIL,this.onRegisterFail);
         RegisterControl.instance.submitRegister(_loc2_,_loc3_);
      }
      
      private function onRegisterFail(param1:RegisterFailEvent) : void
      {
         this._registerBtn.mouseEnabled = true;
         var _loc2_:String = RegisterErrorCode.getErrorCodeMsg(param1.errorCode);
         if(_loc2_ == "")
         {
            _loc2_ = param1.errorCode.toString();
         }
         this.showAlertPanel("注册失败  " + _loc2_,this.hideAlert);
         this._captchaComp.refreshCaptcha();
      }
      
      private function onRegisterReturn(param1:RegisterSuccessEvent) : void
      {
         TongjiUtil.sendTongji(0,param1.mimiNum.toString());
         this._registerBtn.mouseEnabled = true;
         this._mimiNum = param1.mimiNum;
         this.showRegisterSuccessPanel(param1.mimiNum,this._passwordTxt.text);
      }
      
      private function onChageCaptchaBtnClick(param1:MouseEvent) : void
      {
         this._changeCaptchaBtn.mouseEnabled = false;
         this._captchaComp.refreshCaptcha();
      }
      
      private function onApplyRegisterSuccess() : void
      {
         this.clear();
         dispatchEvent(new Event("register_success"));
      }
      
      private function clear() : void
      {
         this.hideAlert();
         this._passWordErrorTxt.text = "";
         this._passwordTxt.text = "";
         this._repatePasswordErrorTxt.text = "";
         this._repatePasswordTxt.text = "";
         this._authCodeErrorTxt.text = "";
         this._authCodeTxt.text = "";
      }
      
      private function showAlertPanel(param1:String, param2:Function, param3:Function = null) : void
      {
         this._alertPanel.setTxt(param1,param2,param3);
         addChild(this._alertPanel);
      }
      
      private function hideAlert() : void
      {
         if(Boolean(this._alertPanel) && contains(this._alertPanel))
         {
            removeChild(this._alertPanel);
         }
      }
      
      private function showRegisterSuccessPanel(param1:int, param2:String) : void
      {
         if(this._registerSuccessPanel == null)
         {
            this._registerSuccessPanel = new RegisterSuccessPanel(this.loginNow,this.savePassword);
            this._registerSuccessPanel.x = (960 - this._registerSuccessPanel.width) / 2;
            this._registerSuccessPanel.y = (560 - this._registerSuccessPanel.height) / 2;
         }
         this._registerSuccessPanel.setRegisterInfo(param1,param2);
         addChild(this._registerSuccessPanel);
         this._passWord = param2;
         removeChild(this._mainUI);
         TongjiUtil.sendTongji(1,param1.toString());
      }
      
      private function loginNow(param1:uint, param2:String) : void
      {
         this.destory();
         Login.inst.showPage(2,{
            "type":1,
            "userID":param1,
            "remID":true,
            "remPwd":true,
            "pwd":param2,
            "autoLogin":true
         });
      }
      
      private function savePassword() : void
      {
         this.showAlertPanel("是否把米米号和密码保存在电脑中?   如果<font color=\'#FF0000\'>不是自己的电脑请不要保存密码！</font>",this.doSavePassword,this.cancleFun);
      }
      
      private function hideRegisterSuccessAlert() : void
      {
         if(Boolean(this._registerSuccessPanel) && contains(this._registerSuccessPanel))
         {
            this._registerSuccessPanel.clear();
            removeChild(this._registerSuccessPanel);
         }
      }
      
      private function doSavePassword() : void
      {
         if(this.file == null)
         {
            this.file = new FileReference();
         }
         var _loc1_:ByteArray = this._registerSuccessPanel.getRegisterInfoArr();
         this.file.save(_loc1_,"我的米米号 -" + this._mimiNum + ".jpg");
         this.hideAlert();
      }
      
      private function cancleFun() : void
      {
         this.hideAlert();
      }
      
      public function get mimiNum() : int
      {
         return this._mimiNum;
      }
      
      public function get passWord() : String
      {
         return this._passWord;
      }
      
      public function destory() : void
      {
         RegisterControl.instance.removeEventListener(RegisterSuccessEvent.REGISTER_SUCCESS,this.onRegisterReturn);
         RegisterControl.instance.removeEventListener(RegisterFailEvent.REGISTER_FAIL,this.onRegisterFail);
         if(this._registerSuccessPanel)
         {
            this._registerSuccessPanel.destory();
            this._registerSuccessPanel = null;
         }
         if(this._alertPanel)
         {
            this._alertPanel.destory();
            this._alertPanel = null;
         }
         this.removeEvent();
         if(contains(this._mainUI))
         {
            removeChild(this._mainUI);
         }
         this._mainUI = null;
         DisplayUtil.removeForParent(this);
      }
   }
}

