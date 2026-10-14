package com.mole.login
{
   import com.mole.*;
   import com.mole.login.utils.*;
   import flash.display.MovieClip;
   import flash.display.SimpleButton;
   import flash.display.Sprite;
   import flash.events.*;
   import flash.geom.*;
   import flash.text.TextField;
   
   public class LoginAlert extends Sprite
   {
      
      public static const NORMAL_WARN:uint = 1;
      
      public static const NORMAL_ERROR:uint = 2;
      
      public static const SYS_PROMPT:uint = 3;
      
      public static const SYS_ERROR:uint = 4;
      
      public static const HELP_AN:uint = 1;
      
      public static const ENTER_GAME_AN:uint = 2;
      
      public static const MODIFY_PWD_AN:uint = 4;
      
      public static const GOT_AN:uint = 8;
      
      public static const RESET_LOGIN_AN:uint = 16;
      
      private var _alert_mc:Sprite;
      
      private var _sure_btn:SimpleButton;
      
      private var _no_btn:SimpleButton;
      
      private var _help_btn:SimpleButton;
      
      private var _login_btn:SimpleButton;
      
      private var _modifyPwd_btn:SimpleButton;
      
      private var _got_btn:SimpleButton;
      
      private var _reLogin_btn:SimpleButton;
      
      private var _type_mc:MovieClip;
      
      private var _msg_txt:TextField;
      
      private var _funList:Array;
      
      private var _paramList:Array;
      
      public function LoginAlert(param1:uint, param2:String, param3:uint = 1, param4:Array = null, param5:Array = null)
      {
         var _loc8_:SimpleButton = null;
         super();
         this._alert_mc = new RES_Login_Alert();
         DisplayUtil.align(this._alert_mc,new Rectangle(0,0,960,560),AlignType.MIDDLE_CENTER);
         addChild(this._alert_mc);
         this._funList = new Array();
         this._paramList = new Array();
         this._type_mc = this._alert_mc["type_mc"];
         this._type_mc.gotoAndStop(param1);
         this._sure_btn = this._alert_mc["sure_btn"];
         this._no_btn = this._alert_mc["no_btn"];
         this._help_btn = this._alert_mc["help_btn"];
         this._login_btn = this._alert_mc["login_btn"];
         this._modifyPwd_btn = this._alert_mc["modifyPwd_btn"];
         this._got_btn = this._alert_mc["got_btn"];
         this._reLogin_btn = this._alert_mc["reLogin_btn"];
         this._sure_btn.visible = false;
         this._no_btn.visible = false;
         this._help_btn.visible = false;
         this._login_btn.visible = false;
         this._modifyPwd_btn.visible = false;
         this._got_btn.visible = false;
         this._reLogin_btn.visible = false;
         var _loc6_:Array = new Array();
         var _loc7_:uint = 0;
         if(param3 == 0)
         {
            this._funList[0] = param4[_loc7_];
            this._paramList[0] = param5[_loc7_];
            _loc7_++;
            _loc6_.push(this._sure_btn);
         }
         if(param3 == 0)
         {
            this._funList[1] = param4[_loc7_];
            this._paramList[1] = param5[_loc7_];
            _loc7_++;
            _loc6_.push(this._no_btn);
         }
         if(HELP_AN & param3)
         {
            this._funList[0] = param4[_loc7_];
            this._paramList[0] = param5[_loc7_];
            _loc7_++;
            _loc6_.push(this._help_btn);
         }
         if(MODIFY_PWD_AN & param3)
         {
            this._funList[2] = param4[_loc7_];
            this._paramList[2] = param5[_loc7_];
            _loc7_++;
            _loc6_.push(this._modifyPwd_btn);
         }
         if(ENTER_GAME_AN & param3)
         {
            this._funList[1] = param4[_loc7_];
            this._paramList[1] = param5[_loc7_];
            _loc7_++;
            _loc6_.push(this._login_btn);
         }
         if(RESET_LOGIN_AN & param3)
         {
            this._funList[4] = param4[_loc7_];
            this._paramList[4] = param5[_loc7_];
            _loc7_++;
            _loc6_.push(this._reLogin_btn);
         }
         if(GOT_AN & param3)
         {
            this._funList[3] = param4[_loc7_];
            this._paramList[3] = param5[_loc7_];
            _loc7_++;
            _loc6_.push(this._got_btn);
         }
         if(_loc6_.length == 1)
         {
            _loc8_ = _loc6_[0];
            _loc8_.x = 108;
            _loc8_.y = 163;
            _loc8_.visible = true;
         }
         else if(_loc6_.length == 2)
         {
            _loc8_ = _loc6_[0];
            _loc8_.x = 50;
            _loc8_.y = 163;
            _loc8_.visible = true;
            _loc8_ = _loc6_[1];
            _loc8_.x = 158;
            _loc8_.y = 163;
            _loc8_.visible = true;
         }
         this._msg_txt = this._alert_mc["msg_txt"];
         this._msg_txt.text = param2;
         this._sure_btn.addEventListener(MouseEvent.CLICK,this.onHelp);
         this._no_btn.addEventListener(MouseEvent.CLICK,this.onLogin);
         this._help_btn.addEventListener(MouseEvent.CLICK,this.onHelp);
         this._login_btn.addEventListener(MouseEvent.CLICK,this.onLogin);
         this._modifyPwd_btn.addEventListener(MouseEvent.CLICK,this.onModifyPwd);
         this._got_btn.addEventListener(MouseEvent.CLICK,this.onGot);
         this._reLogin_btn.addEventListener(MouseEvent.CLICK,this.onReLogin);
      }
      
      public static function show(param1:uint, param2:String, param3:uint, param4:Array = null, param5:Array = null) : void
      {
         param2 = "    " + param2;
         if(Boolean(param1 & SYS_ERROR) || Boolean(param1 & SYS_PROMPT))
         {
            param2 = "\n" + param2;
         }
         param4 = param4 == null ? [] : param4;
         param5 = param5 == null ? [] : param5;
         var _loc6_:LoginAlert = new LoginAlert(param1,param2,param3,param4,param5);
         Login.inst.addChild(_loc6_);
      }
      
      private function onHelp(param1:MouseEvent) : void
      {
         var _loc2_:Function = this._funList[0];
         var _loc3_:Array = this._paramList[0];
         if(_loc2_ != null)
         {
            _loc2_.apply(null,_loc3_);
         }
         this.destroy();
      }
      
      private function onLogin(param1:MouseEvent) : void
      {
         var _loc2_:Function = this._funList[1];
         var _loc3_:Array = this._paramList[1];
         if(_loc2_ != null)
         {
            _loc2_.apply(null,_loc3_);
         }
         this.destroy();
      }
      
      private function onModifyPwd(param1:MouseEvent) : void
      {
         var _loc2_:Function = this._funList[2];
         var _loc3_:Array = this._paramList[2];
         if(_loc2_ != null)
         {
            _loc2_.apply(null,_loc3_);
         }
         this.destroy();
      }
      
      private function onGot(param1:MouseEvent) : void
      {
         var _loc2_:Function = this._funList[3];
         var _loc3_:Array = this._paramList[3];
         if(_loc2_ != null)
         {
            _loc2_.apply(null,_loc3_);
         }
         this.destroy();
      }
      
      private function onReLogin(param1:MouseEvent) : void
      {
         var _loc2_:Function = this._funList[4];
         var _loc3_:Array = this._paramList[4];
         if(_loc2_ != null)
         {
            _loc2_.apply(null,_loc3_);
         }
         this.destroy();
      }
      
      public function destroy() : void
      {
         this._help_btn.removeEventListener(MouseEvent.CLICK,this.onHelp);
         this._login_btn.removeEventListener(MouseEvent.CLICK,this.onLogin);
         this._modifyPwd_btn.removeEventListener(MouseEvent.CLICK,this.onModifyPwd);
         this._got_btn.removeEventListener(MouseEvent.CLICK,this.onGot);
         this._reLogin_btn.removeEventListener(MouseEvent.CLICK,this.onReLogin);
         DisplayUtil.removeForParent(this._alert_mc);
      }
   }
}

