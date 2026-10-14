package com.mole.login
{
   import com.mole.*;
   import com.mole.login.info.*;
   import com.mole.login.net.*;
   import com.mole.login.type.*;
   import com.mole.login.utils.*;
   import flash.display.*;
   import flash.events.*;
   import flash.net.URLRequest;
   import flash.text.TextField;
   import flash.ui.*;
   import flash.utils.*;
   
   public class LoginServerPage extends PageBase
   {
      
      public static const MAX_SER:uint = 600;
      
      public static var GO_BL:Boolean = false;
      
      private const CanNotTalkServer:Array = [];
      
      private var _title_mc:MovieClip;
      
      private var _id_txt:TextField;
      
      private var _go_btn:SimpleButton;
      
      private var _showAll_btn:SimpleButton;
      
      private var _backFirst_btn:SimpleButton;
      
      private var _serverListCon:Sprite;
      
      private var _menu:LoginServerMenu;
      
      private var _serverAdvList:Array;
      
      private var _serverList:Array;
      
      private var _serverListBar:ScrollBar;
      
      private var _advertisementMC:MovieClip;
      
      private var _advTimer:Timer;
      
      private var _fast_btn:SimpleButton;
      
      private var _serverNodeList:Array;
      
      public function LoginServerPage()
      {
         super(new RES_Login_SelectServer());
         this._title_mc = _page_mc["title_mc"];
         this._fast_btn = _page_mc["fast_btn"];
         this._fast_btn.addEventListener(MouseEvent.CLICK,this.onFastBtn);
         this._id_txt = _page_mc["serverId_txt"];
         this._go_btn = _page_mc["go_btn"];
         this._showAll_btn = _page_mc["showAll_btn"];
         this._showAll_btn.addEventListener(MouseEvent.CLICK,this.onShowAll);
         this._backFirst_btn = _page_mc["backfirst_btn"];
         this._backFirst_btn.addEventListener(MouseEvent.CLICK,this.onBackFirstAll);
         this._showAll_btn.visible = true;
         this._backFirst_btn.visible = false;
         this._serverListCon = _page_mc["serverListCon"];
         this._menu = new LoginServerMenu(_page_mc["menu_mc"],this);
         this._menu.hide();
         this._id_txt.addEventListener(FocusEvent.FOCUS_IN,this.onIDFocusIn);
         this._id_txt.addEventListener(FocusEvent.FOCUS_OUT,this.onIDFocusOut);
         this._id_txt.addEventListener(KeyboardEvent.KEY_DOWN,this.onIDKeyDown);
         this._go_btn.addEventListener(MouseEvent.CLICK,this.onGoServer);
         LoginPktParser.GetRecomServers();
         TongjiUtil.sendTongji(4,TongjiUtil.nowUserId.toString());
         LoginSocket.addCmdListener(LoginCmd.CMD_GET_GOOD_SERVER_LIST,this.onGetGoodServerList,this.onGetGoodServerListError);
      }
      
      private function removeAdvertisement(param1:TimerEvent = null) : void
      {
         if(this._advTimer)
         {
            this._advTimer.stop();
            BC.removeEvent(this,this._advTimer);
            this._advTimer = null;
         }
         if(param1 != null)
         {
            this.get100server();
         }
         if(this._advertisementMC)
         {
            DisplayUtil.removeForParent(this._advertisementMC);
         }
      }
      
      private function get100server() : void
      {
         var _loc1_:int = Math.ceil(Math.random() * 20);
         GO_BL = false;
      }
      
      private function onGetServerListAdv(param1:EventTaomee) : void
      {
         var _loc5_:uint = 0;
         var _loc6_:uint = 0;
         LoginSocket.removeCmdListener(LoginCmd.CMD_GET_SERVER_LIST,this.onGetServerListAdv);
         var _loc2_:GetServerListProtocol = param1.EventObj as GetServerListProtocol;
         this._serverAdvList = _loc2_.serverList;
         var _loc3_:uint = 0;
         var _loc4_:int = 5;
         var _loc7_:ServerInfo = this._serverAdvList[0];
         var _loc8_:uint = 0;
         while(_loc8_ < this._serverAdvList.length)
         {
            _loc5_ = uint(this._serverAdvList[_loc8_].userCount);
            _loc6_ = _loc7_.userCount;
            if(_loc6_ == 5)
            {
               _loc6_ = 0;
            }
            if(_loc5_ < _loc4_)
            {
               if(_loc5_ > _loc6_)
               {
                  _loc7_ = this._serverAdvList[_loc8_];
               }
            }
            _loc8_++;
         }
         this.selectServer(_loc7_);
      }
      
      private function addAdvertisementPanel() : void
      {
         this._advertisementMC = new MovieClip();
         addChild(this._advertisementMC);
         this._advTimer = new Timer(288000);
         BC.addEvent(this,this._advTimer,TimerEvent.TIMER,this.removeAdvertisement);
         this._advTimer.start();
         this.loadAdvertisement("resource/login/2021ment.swf");
         this.loadAdvertisement("resource/login/2022ment.swf");
      }
      
      private function loadAdvertisement(param1:String) : void
      {
         var urlReq:URLRequest;
         var loaderInfo:LoaderInfo = null;
         var url:String = param1;
         var loader:Loader = new Loader();
         loaderInfo = loader.contentLoaderInfo;
         loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR,function failFun(param1:IOErrorEvent):void
         {
            loaderInfo.removeEventListener(IOErrorEvent.IO_ERROR,failFun);
         });
         loader.contentLoaderInfo.addEventListener(Event.COMPLETE,function succFun(param1:Event):void
         {
            var nn:int;
            var MC:MovieClip = null;
            var closeHandler:Function = null;
            var enterHandler:Function = null;
            var e:Event = param1;
            loaderInfo.removeEventListener(Event.COMPLETE,succFun);
            MC = loaderInfo.content as MovieClip;
            nn = Math.random() * MC.totalFrames + 1;
            MC.gotoAndStop(nn);
            _advertisementMC.addChild(MC);
            closeHandler = function(param1:MouseEvent):void
            {
               _advertisementMC.removeChild(MC);
               MC["close_btn"].removeEventListener(MouseEvent.CLICK,closeHandler);
               MC = null;
            };
            enterHandler = function(param1:MouseEvent):void
            {
               _advertisementMC.removeChild(MC);
               MC["enter_btn"].removeEventListener(MouseEvent.CLICK,enterHandler);
               MC = null;
               get100server();
            };
            MC["close_btn"].addEventListener(MouseEvent.CLICK,closeHandler);
            MC["enter_btn"].addEventListener(MouseEvent.CLICK,enterHandler);
         });
         urlReq = VersionManager.getURLRequest(url);
         loader.load(urlReq);
      }
      
      private function onGetGoodServerListError(param1:EventTaomee) : void
      {
         LoginDebug.inst.write("拉取推荐服务器列表 出错");
         var _loc2_:LoginResPkt = param1.EventObj as LoginResPkt;
         if(_loc2_.errorID == 5005)
         {
            LoginPktParser.CreateMole();
         }
      }
      
      private function onIDKeyDown(param1:KeyboardEvent) : void
      {
         var _loc2_:String = null;
         if(param1.keyCode == Keyboard.ENTER)
         {
            _loc2_ = this._id_txt.text;
            this.searchServerID(_loc2_);
            StatisticsManager.send(471);
         }
      }
      
      private function onIDFocusIn(param1:FocusEvent) : void
      {
         this._id_txt.textColor = 0;
         if(this._id_txt.text == "请输入服务器名称")
         {
            this._id_txt.text = "";
         }
      }
      
      private function onIDFocusOut(param1:FocusEvent) : void
      {
         if(!this._id_txt.text)
         {
            this._id_txt.textColor = 10066329;
            this._id_txt.text = "请输入服务器名称";
         }
      }
      
      private function onGoServer(param1:MouseEvent) : void
      {
         var _loc2_:String = this._id_txt.text;
         this.searchServerID(_loc2_);
         StatisticsManager.send(472);
      }
      
      private function searchServerID(param1:String) : void
      {
         var _loc2_:ServerInfo = null;
         var _loc3_:ServerInfo = null;
         var _loc4_:uint = 0;
         if(param1)
         {
            for each(_loc3_ in this._serverList)
            {
               if(uint(param1) == _loc3_.id || param1 == _loc3_.name)
               {
                  _loc2_ = _loc3_;
                  break;
               }
            }
            if(_loc2_)
            {
               this.selectServer(_loc2_);
            }
            else
            {
               _loc4_ = uint(param1);
               if(_loc4_ < 1 || _loc4_ > MAX_SER)
               {
                  LoginAlert.show(LoginAlert.SYS_PROMPT,"服务器不存在，请选择其它服务器！",LoginAlert.GOT_AN);
               }
               else
               {
                  GO_BL = true;
                  LoginSocket.addCmdListener(LoginCmd.CMD_GET_SERVER_LIST,this.onGetServerList);
                  LoginPktParser.GetAllServers(_loc4_,_loc4_);
               }
            }
         }
         else
         {
            LoginAlert.show(LoginAlert.SYS_PROMPT,"请输入服务器名或编号！",LoginAlert.GOT_AN);
         }
      }
      
      private function onGetServerList(param1:EventTaomee) : void
      {
         if(_page_mc["menu_mc"].visible == false)
         {
            LoginSocket.removeCmdListener(LoginCmd.CMD_GET_SERVER_LIST,this.onGetServerList);
         }
         LoginDebug.inst.write("拉取推荐服务器列表");
         var _loc2_:GetServerListProtocol = param1.EventObj as GetServerListProtocol;
         this._serverList = _loc2_.serverList;
         if(GO_BL)
         {
            this.selectServer(this._serverList[0]);
            GO_BL = false;
         }
         else
         {
            this.update();
         }
      }
      
      private function onFastBtn(param1:MouseEvent) : void
      {
         this.get100server();
      }
      
      private function onShowAll(param1:MouseEvent) : void
      {
         this._showAll_btn.visible = false;
         this._backFirst_btn.visible = true;
         this._menu.show();
         GO_BL = false;
         LoginSocket.addCmdListener(LoginCmd.CMD_GET_SERVER_LIST,this.onGetServerList);
         LoginPktParser.GetAllServers(1,100);
      }
      
      private function onBackFirstAll(param1:MouseEvent) : void
      {
         this._showAll_btn.visible = true;
         this._backFirst_btn.visible = false;
         this._menu.hide();
         LoginPktParser.GetRecomServers();
         StatisticsManager.send(470);
      }
      
      private function onGetGoodServerList(param1:EventTaomee) : void
      {
         var _loc2_:GetGoodServerListProtocol = param1.EventObj as GetGoodServerListProtocol;
         this._serverList = _loc2_.serverList;
         this.update();
         this.addAdvertisementPanel();
      }
      
      private function update() : void
      {
         var _loc1_:MovieClip = null;
         var _loc2_:ServerInfo = null;
         var _loc4_:Number = Number(NaN);
         if(this._serverListBar)
         {
            this._serverListBar.clearClass();
            this._serverListBar = null;
            if(this._serverListCon.mask)
            {
               this._serverListCon.mask = null;
            }
         }
         DisplayUtil.removeAllChild(this._serverListCon);
         if(this._serverNodeList)
         {
            for each(_loc1_ in this._serverNodeList)
            {
               _loc1_.removeEventListener(MouseEvent.CLICK,this.onEnterServer);
            }
         }
         this._serverNodeList = [];
         this._serverListCon.x = 52;
         this._serverListCon.y = 74;
         var _loc3_:uint = 0;
         while(_loc3_ < this._serverList.length)
         {
            _loc2_ = this._serverList[_loc3_];
            _loc1_ = new RES_Login_OneServer();
            _loc1_["num_txt"].text = _loc2_.id.toString();
            _loc1_["name_txt"].text = LoginServerConfig.inst.getServerName(_loc2_.id);
            _loc1_["state_mc"].gotoAndStop(_loc2_.userCount + 1);
            if(_loc2_.flag == 1)
            {
               _loc1_.findshow_mc.gotoAndStop(3);
            }
            else if(this.CanNotTalkServer.indexOf(_loc2_.id) < 0)
            {
               if(_loc2_.friends > 0)
               {
                  _loc1_.findshow_mc.gotoAndStop(2);
               }
               else
               {
                  _loc1_.findshow_mc.gotoAndStop(1);
               }
            }
            _loc1_.mouseChildren = false;
            _loc1_.buttonMode = true;
            _loc1_.addEventListener(MouseEvent.CLICK,this.onEnterServer);
            _loc1_.serverInfo = _loc2_;
            _loc1_.x = _loc3_ % 2 * 365 + 2;
            _loc1_.y = Math.floor(_loc3_ / 2) * 58 + 2;
            this._serverListCon.addChild(_loc1_);
            _loc3_++;
         }
         if(this._serverList.length > 10)
         {
            _loc4_ = 280;
            this._serverListBar = new ScrollBar(null,this._serverListCon,{
               "size":28,
               "length":_loc4_,
               "x":760,
               "y":this._serverListCon.y
            },ScrollBar.ENABLE_ABATE,ScrollBar.DIRECTION_VERTICAL,_loc4_);
         }
      }
      
      private function onEnterServer(param1:MouseEvent) : void
      {
         var _loc2_:MovieClip = param1.currentTarget as MovieClip;
         var _loc3_:ServerInfo = _loc2_.serverInfo;
         this.selectServer(_loc3_);
      }
      
      public function selectServer(param1:ServerInfo) : void
      {
         var _loc2_:String = null;
         if(param1)
         {
            if(param1.userCount == 5 && !LoginData.isVip)
            {
               _loc2_ = "  抱歉" + LoginServerConfig.inst.getServerName(param1.id) + "已满，请选择其它服务器!";
               LoginAlert.show(LoginAlert.NORMAL_WARN,_loc2_,LoginAlert.GOT_AN);
            }
            else
            {
               LoginData.ip = param1.ip;
               LoginData.port = param1.port;
               LoginData.serverID = param1.id;
               Login.inst.enterGame();
            }
         }
         else
         {
            LoginAlert.show(LoginAlert.SYS_PROMPT,"服务器不存在，请选择其它服务器！",LoginAlert.GOT_AN);
         }
      }
      
      override public function destroy() : void
      {
         this._go_btn.removeEventListener(MouseEvent.CLICK,this.onGoServer);
         this._id_txt.removeEventListener(FocusEvent.FOCUS_IN,this.onIDFocusIn);
         this._id_txt.removeEventListener(KeyboardEvent.KEY_DOWN,this.onIDKeyDown);
         this._id_txt.removeEventListener(FocusEvent.FOCUS_OUT,this.onIDFocusOut);
         this._menu.destroy();
         this._showAll_btn.removeEventListener(MouseEvent.CLICK,this.onShowAll);
         this._backFirst_btn.removeEventListener(MouseEvent.CLICK,this.onBackFirstAll);
         this._fast_btn.removeEventListener(MouseEvent.CLICK,this.onFastBtn);
         LoginSocket.removeCmdListener(LoginCmd.CMD_GET_SERVER_LIST,this.onGetServerList);
         LoginSocket.removeCmdListener(LoginCmd.CMD_GET_SERVER_LIST,this.onGetServerListAdv);
         LoginSocket.removeCmdListener(LoginCmd.CMD_GET_GOOD_SERVER_LIST,this.onGetGoodServerList,this.onGetGoodServerListError);
         this.removeAdvertisement();
         super.destroy();
      }
   }
}

