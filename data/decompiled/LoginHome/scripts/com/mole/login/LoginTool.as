package com.mole.login
{
   import com.mole.*;
   import com.mole.login.utils.*;
   import flash.display.*;
   import flash.events.*;
   import flash.media.Sound;
   import flash.net.*;
   
   public class LoginTool extends Sprite
   {
      
      private var _tool_mc:Sprite;
      
      private var _app_btn:SimpleButton;
      
      private var _create_btn:SimpleButton;
      
      private var _intro_btn:SimpleButton;
      
      private var _collect_btn:SimpleButton;
      
      private var _login_btn:SimpleButton;
      
      private var _star_btn:SimpleButton;
      
      private var _bbs_btn:SimpleButton;
      
      private var _mole_mc:MovieClip;
      
      private var _famknow_btn:SimpleButton;
      
      public function LoginTool()
      {
         super();
         this._tool_mc = new RES_Login_Panel();
         addChild(this._tool_mc);
         this._create_btn = this._tool_mc["create_btn"];
         this._intro_btn = this._tool_mc["intro_btn"];
         this._collect_btn = this._tool_mc["collect_btn"];
         this._login_btn = this._tool_mc["login_btn"];
         this._bbs_btn = this._tool_mc["bbs_btn"];
         this._famknow_btn = this._tool_mc["famknow_btn"];
         this._create_btn.addEventListener(MouseEvent.CLICK,this.onOpenCreate);
         this._intro_btn.addEventListener(MouseEvent.CLICK,this.onOpenIntro);
         this._collect_btn.addEventListener(MouseEvent.CLICK,this.onCollect);
         this._login_btn.addEventListener(MouseEvent.CLICK,this.onLogin);
         this._bbs_btn.addEventListener(MouseEvent.CLICK,this.onOpenBBs);
         this._famknow_btn.addEventListener(MouseEvent.CLICK,this.onOpenFamKnow);
      }
      
      private function playAn() : void
      {
         var _loc1_:Sound = new RES_Login_An_Sound();
         _loc1_.play();
      }
      
      private function onOpenBook(param1:MouseEvent) : void
      {
         this.playAn();
         navigateToURL(new URLRequest("http://mf.61.com/"),"_blank");
      }
      
      private function onOpenStar(param1:MouseEvent) : void
      {
         this.playAn();
         navigateToURL(new URLRequest("http://mf.61.com"),"_blank");
      }
      
      private function onOpenFamKnow(param1:MouseEvent) : void
      {
         this.playAn();
         navigateToURL(new URLRequest("http://parents.61.com/care"),"_blank");
      }
      
      private function onOpenBBs(param1:MouseEvent) : void
      {
         LoginStatisticsManager.send(272);
         this.playAn();
         navigateToURL(new URLRequest("http://mf.61.com"),"_blank");
      }
      
      private function onOpenApp(param1:MouseEvent) : void
      {
         this.playAn();
         navigateToURL(new URLRequest("http://mf.61.com"),"_blank");
      }
      
      private function onOpenCreate(param1:MouseEvent) : void
      {
         LoginStatisticsManager.send(271);
         this.playAn();
         navigateToURL(new URLRequest("https://account.61.com/register"),"_blank");
      }
      
      private function onOpenIntro(param1:MouseEvent) : void
      {
         this.playAn();
         LoginStatisticsManager.send(274);
         navigateToURL(new URLRequest("http://kf.61.com"),"_blank");
      }
      
      private function onLoaderNoteComplete(param1:Event) : void
      {
         var _loc2_:LoaderInfo = param1.currentTarget as LoaderInfo;
         _loc2_.removeEventListener(Event.COMPLETE,this.onLoaderNoteComplete);
         LoginHome.inst.hideLoading();
         var _loc3_:DisplayObjectContainer = LoginHome.inst;
         if(_loc3_)
         {
            _loc3_.addChild(_loc2_.content);
         }
      }
      
      private function onCollect(param1:MouseEvent) : void
      {
         this.playAn();
         StatisticsManager.send(452);
         this.playAn();
         navigateToURL(new URLRequest("http://mf.61.com"),"_blank");
      }
      
      private function onLogin(param1:MouseEvent) : void
      {
         this.playAn();
         dispatchEvent(new Event(LoginHome.START_LOGIN));
         LoginStatisticsManager.send(270);
      }
      
      public function destroy() : void
      {
         this._create_btn.removeEventListener(MouseEvent.CLICK,this.onOpenCreate);
         this._intro_btn.removeEventListener(MouseEvent.CLICK,this.onOpenIntro);
         this._collect_btn.removeEventListener(MouseEvent.CLICK,this.onCollect);
         this._login_btn.removeEventListener(MouseEvent.CLICK,this.onLogin);
         DisplayUtil.removeForParent(this);
      }
   }
}

