package com.mole.login
{
   import com.mole.login.info.*;
   import com.mole.login.net.*;
   import com.mole.login.type.*;
   import com.mole.login.utils.*;
   import flash.display.*;
   import flash.events.*;
   import flash.text.TextField;
   import flash.utils.ByteArray;
   
   public class LoginOneAuthCode
   {
      
      private var _authCode_mc:Sprite;
      
      private var _code_txt:TextField;
      
      private var _get_btn:SimpleButton;
      
      private var _msg_txt:TextField;
      
      private var _authCon:Sprite;
      
      private var _codeID:ByteArray;
      
      public function LoginOneAuthCode(param1:Sprite, param2:uint = 0)
      {
         super();
         this._authCode_mc = param1;
         this._authCode_mc.visible = false;
         this._authCode_mc.y += param2;
         this._authCon = new Sprite();
         this._authCon.mouseChildren = false;
         this._authCon.mouseEnabled = false;
         this._authCode_mc.addChild(this._authCon);
         this._code_txt = this._authCode_mc["code_txt"];
         this._get_btn = this._authCode_mc["get_btn"];
         this._msg_txt = this._authCode_mc["msg_txt"];
         this._get_btn.addEventListener(MouseEvent.CLICK,this.onGetAuthCode);
         LoginSocket.addCmdListener(LoginCmd.CMD_GET_AUTHCODE,this.onGetAuthCodeData);
      }
      
      private function onGetAuthCodeData(param1:EventTaomee) : void
      {
         var _loc2_:GetAuthCodeProtocol = param1.EventObj as GetAuthCodeProtocol;
         if(_loc2_.flag != 0)
         {
            if(_loc2_.flag == 1)
            {
               this._msg_txt.text = "密码错误太多，请输入验证码。";
            }
            else if(_loc2_.flag == 2)
            {
               this._msg_txt.text = "验证码输入错误。";
            }
            else if(_loc2_.flag == 3)
            {
               this._msg_txt.text = "帐号错误。";
            }
            else if(_loc2_.flag == 4)
            {
               this._msg_txt.text = "帐号被封。";
            }
            else if(_loc2_.flag == 5)
            {
               this._msg_txt.text = "系统错误或帐号未实名认证,请登录account.61.com进行实名认证。";
            }
            this.show(_loc2_.codeID,_loc2_.picLoader);
         }
         else
         {
            this._authCode_mc.visible = false;
            LoginOnePage.inst.setAuthCode(false);
         }
      }
      
      public function show(param1:ByteArray, param2:DisplayObject, param3:Boolean = true, param4:int = -5) : void
      {
         this._codeID = param1;
         DisplayUtil.removeAllChild(this._authCon);
         this._authCon.addChild(param2);
         this._authCode_mc.visible = true;
         if(param3)
         {
            param2.x = 158;
            LoginOnePage.inst.setAuthCode(true);
         }
         else
         {
            param2.x = 135;
         }
         param2.y = param4;
      }
      
      private function onGetAuthCode(param1:MouseEvent) : void
      {
         StatisticsManager.send(465);
         LoginPktParser.GetAuthCode();
      }
      
      public function get authObj() : Object
      {
         var _loc1_:Object = null;
         if(this._authCode_mc.visible)
         {
            _loc1_ = new Object();
            _loc1_.codeId = this._codeID;
            _loc1_.value = this._code_txt.text;
            return _loc1_;
         }
         return null;
      }
      
      public function destroy() : void
      {
         DisplayUtil.removeForParent(this._authCon);
         LoginSocket.removeCmdListener(LoginCmd.CMD_GET_AUTHCODE,this.onGetAuthCodeData);
         this._get_btn.removeEventListener(MouseEvent.CLICK,this.onGetAuthCode);
      }
   }
}

