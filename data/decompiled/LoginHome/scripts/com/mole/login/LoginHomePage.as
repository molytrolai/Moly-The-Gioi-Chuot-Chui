package com.mole.login
{
   import com.mole.*;
   import com.mole.login.utils.*;
   import flash.display.*;
   import flash.events.*;
   import flash.media.*;
   import flash.net.*;
   
   public class LoginHomePage extends Sprite
   {
      
      private var _tool:LoginTool;
      
      private var content:DisplayObject;
      
      private var _summerFlvVideo:Video;
      
      private var _summerFlvNetStream:NetStream;
      
      private var _flvMovieContainer:Sprite;
      
      private var _closeBtn:SimpleButton;
      
      public function LoginHomePage()
      {
         var _loc2_:uint = 0;
         var _loc5_:Sprite = null;
         super();
         var _loc1_:uint = 0;
         while(_loc1_ < 1)
         {
            _loc5_ = new Sprite();
            _loc5_.graphics.beginFill(16777215,1);
            _loc5_.graphics.drawRect(0,0,960,560);
            _loc5_.graphics.endFill();
            addChild(_loc5_);
            _loc2_ = uint(VersionManager.getFileSize("module/external/logo/51moleInfo" + _loc1_ + ".swf"));
            if(!_loc2_)
            {
               break;
            }
            _loc1_++;
         }
         var _loc3_:int = Math.floor(Math.random() * _loc1_);
         var _loc4_:Loader = new Loader();
         _loc4_.load(VersionManager.getURLRequest("module/external/logo/51moleInfo" + _loc3_ + ".swf"));
         _loc4_.contentLoaderInfo.addEventListener(Event.COMPLETE,this.loadComplete);
         addChild(_loc4_);
      }
      
      private function loadComplete(param1:Event) : void
      {
         this._tool = new LoginTool();
         this._tool.addEventListener(LoginHome.START_LOGIN,this.onStartLogin);
         addChild(this._tool);
         param1.currentTarget.removeEventListener(Event.COMPLETE,this.loadComplete);
         this.content = LoaderInfo(param1.currentTarget).content;
         if(this.content["playMovie"])
         {
            SimpleButton(this.content["playMovie"]).addEventListener(MouseEvent.CLICK,this.playMovieHandler);
         }
         if(!this._summerFlvVideo)
         {
            this._summerFlvVideo = new Video(960,560);
            this._summerFlvVideo.x = 0;
            this._summerFlvVideo.y = 0;
            this._flvMovieContainer = new Sprite();
            this._flvMovieContainer.graphics.beginFill(0,1);
            this._flvMovieContainer.graphics.drawRect(0,0,960,560);
            this._flvMovieContainer.graphics.endFill();
            this._flvMovieContainer.addChild(this._summerFlvVideo);
         }
         var _loc2_:SharedObject = SharedObject.getLocal("summerFlv");
         if(_loc2_.data.isPlayer)
         {
         }
         _loc2_.data.isPlayer = true;
         _loc2_.flush();
      }
      
      private function playMovieHandler(param1:MouseEvent = null) : void
      {
         addChild(this._flvMovieContainer);
         var _loc2_:NetConnection = new NetConnection();
         _loc2_.connect(null);
         this._summerFlvNetStream = new NetStream(_loc2_);
         this._summerFlvNetStream.client = {"onMetaData":this.onMetaData};
         this._summerFlvNetStream.play(VersionManager.getURL("resource/ui/summerFlv.flv"));
         this._summerFlvVideo.attachNetStream(this._summerFlvNetStream);
         this._summerFlvNetStream.addEventListener(AsyncErrorEvent.ASYNC_ERROR,this.asyncError);
         this._summerFlvNetStream.addEventListener(NetStatusEvent.NET_STATUS,this.netStatusHandler);
      }
      
      private function onMetaData(... rest) : void
      {
      }
      
      private function asyncError(param1:AsyncErrorEvent) : void
      {
      }
      
      private function netStatusHandler(param1:NetStatusEvent) : void
      {
         if(param1.info.code == "NetStream.Play.Stop")
         {
            this.closeVideoHandler();
         }
      }
      
      private function onStartLogin(param1:Event) : void
      {
         dispatchEvent(new Event(LoginHome.START_LOGIN));
      }
      
      private function closeVideoHandler(param1:MouseEvent = null) : void
      {
         this._summerFlvNetStream.removeEventListener(AsyncErrorEvent.ASYNC_ERROR,this.asyncError);
         this._summerFlvNetStream.removeEventListener(NetStatusEvent.NET_STATUS,this.netStatusHandler);
         this._summerFlvVideo.clear();
         this._summerFlvNetStream.close();
         if(this._flvMovieContainer)
         {
            removeChild(this._flvMovieContainer);
         }
      }
      
      public function destroy() : void
      {
         try
         {
            this._summerFlvVideo.clear();
            this._summerFlvVideo = null;
         }
         catch(e:*)
         {
         }
         try
         {
            this._summerFlvNetStream.close();
            this._summerFlvNetStream = null;
         }
         catch(e:*)
         {
         }
         try
         {
            this._closeBtn.removeEventListener(MouseEvent.CLICK,this.closeVideoHandler);
            removeChild(this._flvMovieContainer);
            this._flvMovieContainer = null;
         }
         catch(e:*)
         {
         }
         this._tool.removeEventListener(LoginHome.START_LOGIN,this.onStartLogin);
         this._tool = null;
         DisplayUtil.removeForParent(this);
      }
   }
}

