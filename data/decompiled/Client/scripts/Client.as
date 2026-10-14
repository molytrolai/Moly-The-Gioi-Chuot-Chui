package
{
   import com.taomee.plugins.versionManager.TaomeeVersionManager;
   import flash.display.Loader;
   import flash.display.LoaderInfo;
   import flash.display.MovieClip;
   import flash.display.Sprite;
   import flash.display.StageScaleMode;
   import flash.events.Event;
   import flash.events.IOErrorEvent;
   import flash.events.MouseEvent;
   import flash.events.ProgressEvent;
   import flash.events.TimerEvent;
   import flash.external.ExternalInterface;
   import flash.net.SharedObject;
   import flash.net.URLLoader;
   import flash.net.URLRequest;
   import flash.net.navigateToURL;
   import flash.system.ApplicationDomain;
   import flash.system.Capabilities;
   import flash.system.LoaderContext;
   import flash.system.Security;
   import flash.text.TextField;
   import flash.ui.ContextMenu;
   import flash.ui.ContextMenuItem;
   import flash.utils.Timer;
   import flash.utils.getDefinitionByName;
   import org.taomee.stat.StatisticsManager;
   
   [SWF(width="960", height="560", backgroundColor="#ffffff", frameRate="24")]
   [SWF(frameRate="24",backgroundColor="#ffffff",width="960",height="560")]
   [SWF(frameRate="24",width="960",height="560")]
   public class Client extends Sprite
   {
      
      public static var rndTxtList:Array;
      
      public static var mainLoadBG:MovieClip;
      
      private static var _urlParams:*;
      
      private var _dllLoader:DLLLoader;
      
      private var _loadingPanel:LoadingPanel;
      
      private var _content:Sprite;
      
      private var _gameBg:MovieClip;
      
      private var _debug:Boolean = false;
      
      private var myCookie:SharedObject;
      
      private var _time:uint = 0;
      
      private var _timer:Timer;
      
      private var _resAppDomain:ApplicationDomain;
      
      private var _loaderInfo:LoaderInfo;
      
      private var _isEnterLoginLogic:Boolean = false;
      
      private var _loginLogic:*;
      
      private var _serverXml:XML;
      
      private var _userInfo:Object;
      
      private var _loginData:Object;
      
      public function Client()
      {
         super();
         Security.allowDomain("*");
         stage.stageFocusRect = false;
         stage.scaleMode = StageScaleMode.NO_SCALE;
         StatisticsManager.setup(1);
         StatisticsManager.setEnabled(true);
         this._content = new Sprite();
         addChild(this._content);
         this.showTxt("请稍候，正在进入摩尔庄园...");
         ClientTool.inst.send(256);
         if(Capabilities.playerType == "PlugIn" || Capabilities.playerType == "ActiveX")
         {
            if(ExternalInterface.available)
            {
               this.init();
            }
            else
            {
               this.showError();
            }
         }
         else
         {
            this.init();
         }
         this._timer = new Timer(1000);
         this._timer.addEventListener(TimerEvent.TIMER,this.onTick);
         this._timer.start();
      }
      
      private static function getWebArg(name:String) : String
      {
         if(ExternalInterface.available)
         {
            if(!_urlParams)
            {
               _urlParams = ExternalInterface.call("getUrlParams");
            }
            if(Boolean(_urlParams))
            {
               return _urlParams[name];
            }
         }
         return "";
      }
      
      private function onTick(e:TimerEvent) : void
      {
         ++this._time;
      }
      
      private function showError() : void
      {
         this.showTxt("你正在使用的是非法客户端，为了你的账号安全，请直接访问:<font color=\'#FF0000\'>http://mole.61.com</font>");
         stage.addEventListener(MouseEvent.CLICK,this.onOpen51Mole);
      }
      
      private function onOpen51Mole(event:MouseEvent) : void
      {
         stage.removeEventListener(MouseEvent.CLICK,this.onOpen51Mole);
         var urlRequest:URLRequest = new URLRequest("http://mole.61.com");
         navigateToURL(urlRequest,"_self");
      }
      
      private function init() : void
      {
         TaomeeVersionManager.getInstance().load("version/zzz_config.txt",this.onInitVersion);
      }
      
      private function onHeaderVersion(event:Event = null) : void
      {
         var _contextMenu:ContextMenu = new ContextMenu();
         var contextItem1:ContextMenuItem = new ContextMenuItem("您的Flash播放器版本：" + Capabilities.version);
         var contextItem2:ContextMenuItem = new ContextMenuItem("您的客户端版本：" + this.getVersionView(TaomeeVersionManager.getInstance().lastModifiedDate));
         _contextMenu.hideBuiltInItems();
         _contextMenu.customItems.push(contextItem1);
         _contextMenu.customItems.push(contextItem2);
         contextMenu = _contextMenu;
      }
      
      private function getVersionView(t:Date) : String
      {
         return t.fullYear + "." + (t.month + 1) + "." + t.date + " " + t.hours + ":" + t.minutes + ":" + t.seconds + " " + (t.hours >= 12 ? "PM" : "AM");
      }
      
      private function onInitVersion(event:Event = null) : void
      {
         this.onHeaderVersion(event);
         var urlLoader:URLLoader = new URLLoader();
         urlLoader.addEventListener(Event.COMPLETE,this.onLoaderRndXmlComplete);
         urlLoader.load(TaomeeVersionManager.getInstance().getURLRequest("resource/xml/logo/loadingWord.xml"));
      }
      
      private function onLoaderRndXmlComplete(e:Event) : void
      {
         var urlLoader:URLLoader = e.currentTarget as URLLoader;
         urlLoader.removeEventListener(Event.COMPLETE,this.onLoaderRndXmlComplete);
         var msg:String = urlLoader.data;
         rndTxtList = msg.split("_");
         this.loaderRes("module/external/logo/randomMC.swf",this.onLoaderRndSWFComplete,this.onLoadResFail);
      }
      
      private function onLoaderRndSWFComplete(e:Event) : void
      {
         var loaderInfo:LoaderInfo = e.currentTarget as LoaderInfo;
         this.removeLoader(loaderInfo,this.onLoadResource,this.onLoadResFail,false);
         mainLoadBG = loaderInfo.content as MovieClip;
         this.loaderRes("resource/ui/main_resource.swf",this.onLoadResource,this.onLoadResFail);
         ClientTool.inst.send(257);
      }
      
      private function onLoadResource(e:Event) : void
      {
         var loaderInfo:LoaderInfo = e.currentTarget as LoaderInfo;
         this.removeLoader(loaderInfo,this.onLoadResource,this.onLoadResFail);
         this._resAppDomain = loaderInfo.applicationDomain;
         this.loadLoginHome();
      }
      
      private function addBg() : void
      {
         var LoadingCls:Class = null;
         var loading_mc:Sprite = null;
         if(this._loadingPanel == null)
         {
            this._gameBg = new (this._resAppDomain.getDefinition("RES_BG"))() as MovieClip;
            this._gameBg.mouseChildren = false;
            this._gameBg.mouseEnabled = false;
            addChild(this._gameBg);
            addChild(this._content);
            LoadingCls = this._resAppDomain.getDefinition("mainLoad") as Class;
            loading_mc = new LoadingCls();
            this._loadingPanel = new LoadingPanel(loading_mc);
            addChild(this._loadingPanel);
         }
      }
      
      private function loaderRes(url:String, succFun:Function, failFun:Function, appDomain:ApplicationDomain = null, autoVersion:Boolean = true) : void
      {
         var urlReq:URLRequest = null;
         var loader:Loader = new Loader();
         loader.contentLoaderInfo.addEventListener(Event.COMPLETE,succFun);
         loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR,failFun);
         loader.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS,this.onLoadResProgress);
         if(autoVersion)
         {
            urlReq = TaomeeVersionManager.getInstance().getURLRequest(url);
         }
         else
         {
            urlReq = new URLRequest(url + "?rand=" + Math.random());
         }
         loader.load(urlReq,new LoaderContext(false,appDomain));
      }
      
      private function onLoadResProgress(e:ProgressEvent) : void
      {
         if(Boolean(this._loadingPanel))
         {
            this._loadingPanel.setRate(e.bytesLoaded / e.bytesTotal);
         }
      }
      
      private function removeLoader(loaderInfo:LoaderInfo, succFun:Function, failFun:Function, isRemoveContent:Boolean = true) : void
      {
         if(isRemoveContent)
         {
            ClientTool.removeAllChild(this._content);
         }
         loaderInfo.removeEventListener(Event.COMPLETE,succFun);
         loaderInfo.removeEventListener(IOErrorEvent.IO_ERROR,failFun);
      }
      
      private function loadLoginHome() : void
      {
         var webUID:uint = 0;
         var loginSession:Object = ClientTool.loginSession;
         if(ExternalInterface.available)
         {
            ExternalInterface.call("get_uid");
         }
         if(Boolean(loginSession) || Boolean(webUID))
         {
            this._isEnterLoginLogic = true;
            this.enterLoginLogic();
         }
         else
         {
            this.addBg();
            this.loaderRes("resource/login/LoginHome.swf",this.onLoadHomeSucc,this.onLoadResFail);
            this._loadingPanel.setDesc("正在加载登录首页。。。");
            this._loadingPanel.show();
         }
      }
      
      private function onLoadHomeSucc(e:Event) : void
      {
         var loginHome:* = undefined;
         this._loadingPanel.hide();
         this._loaderInfo = e.currentTarget as LoaderInfo;
         this.removeLoader(this._loaderInfo,this.onLoadHomeSucc,this.onLoadResFail);
         this._loaderInfo.content.addEventListener("enterLogin",this.onEnterLogin);
         this._loaderInfo.content["setVersionManager"](TaomeeVersionManager);
         this._loaderInfo.content["init"]();
         this._content.addChild(this._loaderInfo.content);
         var invitedIP:uint = uint(getWebArg("invite_uid"));
         if(invitedIP != 0)
         {
            loginHome = this._loaderInfo.content;
            loginHome["openRegView"]();
         }
         if(this._time <= 10)
         {
            ClientTool.inst.send(258 + this._time);
         }
         else
         {
            ClientTool.inst.send(269);
         }
         this._timer.removeEventListener(TimerEvent.TIMER,this.onTick);
         this._timer.stop();
         this._timer = null;
         this.enterLoginLogic();
      }
      
      private function onLoadDllFail(e:Event) : void
      {
         this.showTxt("加载核心资源失败，请刷新浏览器。");
      }
      
      private function onLoadResFail(event:IOErrorEvent) : void
      {
         if(Boolean(this._loadingPanel))
         {
            this._loadingPanel.hide();
         }
         var loaderInfo:LoaderInfo = event.currentTarget as LoaderInfo;
         this.removeLoader(loaderInfo,this.onLoadHomeSucc,this.onLoadResFail);
         this._loaderInfo = null;
         ClientTool.inst.send(258);
         this.showTxt("加载基础资源失败，请刷新浏览器。");
      }
      
      private function onEnterLogin(e:Event) : void
      {
         this._loaderInfo.content.removeEventListener("enterLogin",this.onEnterLogin);
         this._loaderInfo = null;
         ClientTool.removeAllChild(this._content);
         var loginHome:Object = e.currentTarget;
         this._userInfo = loginHome["regUserInfo"];
         if(Boolean(this._loginLogic))
         {
            this.showLoginLogic();
         }
         else
         {
            this._isEnterLoginLogic = true;
            this.addBg();
            this._loadingPanel.setDesc("正在加载登录。。。");
            this._loadingPanel.show();
         }
      }
      
      private function enterLoginLogic() : void
      {
         var urlLoader:URLLoader = new URLLoader();
         urlLoader.addEventListener(Event.COMPLETE,this.onLoadServerXmlComplete);
         urlLoader.load(TaomeeVersionManager.getInstance().getURLRequest("config/Server.xml"));
      }
      
      private function onLoadServerXmlComplete(e:Event) : void
      {
         var urlLoader:URLLoader = e.currentTarget as URLLoader;
         urlLoader.removeEventListener(Event.COMPLETE,this.onLoadServerXmlComplete);
         this._serverXml = XML(urlLoader.data);
         var serverIp:String = this._serverXml.taomee.@MOUrl.toString();
         this.loaderRes("resource/login/Login.swf",this.onLoadLoginSucc,this.onLoadResFail);
         if(this._isEnterLoginLogic)
         {
            this.addBg();
            this._loadingPanel.setDesc("正在加载登录。。。");
            this._loadingPanel.show();
         }
      }
      
      private function onLoadLoginSucc(e:Event) : void
      {
         this._loadingPanel.hide();
         this._loaderInfo = e.currentTarget as LoaderInfo;
         this.removeLoader(this._loaderInfo,this.onLoadHomeSucc,this.onLoadResFail,false);
         this._loginLogic = this._loaderInfo.content;
         this._loginLogic["setVersionManager"](TaomeeVersionManager);
         if(this._dllLoader == null)
         {
            this._dllLoader = new DLLLoader();
            this._dllLoader.addEventListener(DLLLoader.LOAD_DLL_ERROR,this.onLoadDllFail);
         }
         if(this._isEnterLoginLogic)
         {
            this.showLoginLogic();
         }
      }
      
      private function showLoginLogic() : void
      {
         this._loginLogic.addEventListener("loginSucc",this.onLoginSucc);
         this._loginLogic["init"](this._serverXml,this._userInfo);
         this._content.addChild(this._loginLogic);
      }
      
      private function onLoginSucc(e:Event) : void
      {
         this.showTxt(String(this._dllLoader));
         this._loginData = this._loginLogic["loginData"];
         ClientTool.removeAllChild(this._content);
         if(this._dllLoader.isSucc)
         {
            this.startGame();
         }
         else
         {
            this._dllLoader.addEventListener(DLLLoader.LOAD_DLL_SUCC,this.onLoadDllOver);
            this._dllLoader.addEventListener(ProgressEvent.PROGRESS,this.onLoadDllProgress);
            this._loadingPanel.setRate(0);
            this._loadingPanel.setDesc("正在加载核心文件。。。");
            this._loadingPanel.show();
         }
      }
      
      private function onLoadDllProgress(e:ProgressEvent) : void
      {
         this._loadingPanel.setRate(this._dllLoader.rate);
      }
      
      private function onLoadDllOver(e:Event) : void
      {
         this.startGame();
      }
      
      private function startGame() : void
      {
         this._debug = this._dllLoader.debug;
         this._dllLoader.removeEventListener(DLLLoader.LOAD_DLL_ERROR,this.onLoadDllFail);
         this._dllLoader.removeEventListener(DLLLoader.LOAD_DLL_SUCC,this.onLoadDllOver);
         this._dllLoader.removeEventListener(ProgressEvent.PROGRESS,this.onLoadDllProgress);
         this._loadingPanel.destroy();
         var MainEntryClass:Class = getDefinitionByName("com.core.MainEntry") as Class;
         var mainEntry:* = new MainEntryClass();
         mainEntry.gameBg = this._gameBg;
         stage.addChild(mainEntry);
         mainEntry.setConfig(TaomeeVersionManager,this._debug);
         mainEntry.init(this._serverXml,this._loginData.serNameDict,DLLLoader.beanData,this._resAppDomain,this._loginData.ip,this._loginData.port,this._loginData.userID,this._loginData.session,this._loginData.serverID,this._loginData.serverList,this._dllLoader.dllArrayByte,this._loginData.type,this._loginData.adByte);
         if(this._debug)
         {
            new Stats(stage);
         }
         this._loaderInfo = null;
         this._loadingPanel = null;
         this._dllLoader = null;
         this._loginData = null;
         this._loginLogic = null;
      }
      
      private function showTxt(msg:String) : void
      {
         ClientTool.removeAllChild(this._content);
         var bgTxt:TextField = new TextField();
         bgTxt.autoSize = "center";
         bgTxt.htmlText = "<font size=\'18\'>" + msg + "</font>";
         bgTxt.x = (ClientTool.STAGE_WIDTH - bgTxt.textWidth) / 2;
         bgTxt.y = ClientTool.STAGE_HEIGHT / 2 - 50;
         bgTxt.mouseEnabled = false;
         this._content.addChild(bgTxt);
      }
   }
}

