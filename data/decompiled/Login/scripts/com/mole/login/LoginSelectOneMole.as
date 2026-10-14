package com.mole.login
{
   import com.mole.login.utils.*;
   import flash.display.Sprite;
   import flash.events.*;
   import flash.net.SharedObject;
   import flash.text.TextField;
   
   public class LoginSelectOneMole extends PageBase
   {
      
      public var angle:Number;
      
      private var _nick_txt:TextField;
      
      private var _id_txt:TextField;
      
      private var _prevView:PrevView;
      
      private var _info:Object;
      
      public function LoginSelectOneMole()
      {
         super(new Login_bodyOne_UI());
         _page_mc.visible = false;
         _page_mc.addEventListener(MouseEvent.CLICK,this.onClickNode);
         this._nick_txt = _page_mc["nick_txt"];
         this._id_txt = _page_mc["id_txt"];
         this._prevView = new PrevView(_page_mc);
      }
      
      private function onClickNode(param1:MouseEvent) : void
      {
         dispatchEvent(param1);
      }
      
      public function setInfo(param1:Object) : void
      {
         var _loc2_:SharedObject = null;
         var _loc3_:Array = null;
         this._info = param1;
         if(this._info)
         {
            if(this._info.nick)
            {
               this._nick_txt.text = this._info.nick;
            }
            else
            {
               this._nick_txt.text = this._info.userID;
            }
            if(this._info.userCode)
            {
               this._id_txt.text = this._info.userCode;
            }
            else
            {
               this._id_txt.text = this._info.userID;
            }
            _loc2_ = MoleSharedObject.getMoleData(this._info.userID);
            _loc3_ = _loc2_.data.clothArray;
            this._prevView.setRoleType(this._info.roleType);
            if(_loc2_.data.Family)
            {
               this._prevView.setColor(_loc2_.data.Family);
            }
            else
            {
               this._prevView.setColor(16624949);
            }
            if(_loc3_)
            {
               this._prevView.setCloths(_loc3_);
            }
         }
         else
         {
            this._prevView.setColor(16624949);
            _page_mc["body_mc"].visible = false;
            this._id_txt.visible = false;
            this._nick_txt.visible = false;
         }
         _page_mc.visible = true;
         _page_mc["bgMC"].visible = true;
      }
      
      public function get info() : Object
      {
         return this._info;
      }
      
      override public function destroy() : void
      {
         _page_mc.removeEventListener(MouseEvent.CLICK,this.onClickNode);
         super.destroy();
      }
      
      public function get node_mc() : Sprite
      {
         return _page_mc;
      }
   }
}

