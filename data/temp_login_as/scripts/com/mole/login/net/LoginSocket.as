package com.mole.login.net
{
   import com.mole.*;
   import com.mole.login.*;
   import com.mole.login.info.*;
   import com.mole.login.type.*;
   import com.mole.login.utils.*;
   import flash.display.MovieClip;
   import flash.events.*;
   import flash.geom.*;
   import flash.net.*;
   import flash.utils.*;
   
   public class LoginSocket extends EventDispatcher
   {
      
      private static var _instance:LoginSocket;
      
      private static var _eventDispatcher:EventDispatcher;
      
      public static const OnSocketConnected:String = "OnSocketConnected";
      
      public static const OnSocketIO_ERROR:String = "OnSocketIO_ERROR";
      
      private var _cmdSocktDic:Dictionary = new Dictionary();
      
      private var _errSocketResultDic:Dictionary = new Dictionary();
      
      private const MSG_FIRST_TOKEN_LEN:int = 4;
      
      private var _tempBuffer:ByteArray;
      
      private var _chunkBuffer:ByteArray;
      
      private var _socket:Socket;
      
      private var _host:String;
      
      private var _port:uint;
      
      private var _ipIdx:uint = 0;
      
      private var IP_LIST:Array = ["123.150.163.99","125.39.236.145"];
      
      private var _queueCount:uint = 0;
      
      private var _loading_mc:MovieClip;
      
      private var _oldData:ByteArray;
      
      private var _waitSocketTimeID:uint;
      
      public function LoginSocket()
      {
         super(this);
         this._loading_mc = new RES_Login_Loading();
         DisplayUtil.align(this._loading_mc,new Rectangle(0,0,960,560),AlignType.MIDDLE_CENTER);
         this.initialize();
      }
      
      public static function get instance() : LoginSocket
      {
         if(_instance == null)
         {
            _instance = new LoginSocket();
         }
         return _instance;
      }
      
      private static function onRefreshPage() : void
      {
         navigateToURL(new URLRequest("http://mole.61.com"),"_self");
      }
      
      private static function getEventDispathcer() : EventDispatcher
      {
         if(_eventDispatcher == null)
         {
            _eventDispatcher = new EventDispatcher();
         }
         return _eventDispatcher;
      }
      
      public static function addCmdListener(param1:uint, param2:Function, param3:Function = null) : void
      {
         getEventDispathcer().addEventListener("Socket_" + param1,param2);
         if(param3 != null)
         {
            getEventDispathcer().addEventListener("SocketError_" + param1,param3);
         }
      }
      
      public static function removeCmdListener(param1:uint, param2:Function, param3:Function = null) : void
      {
         getEventDispathcer().removeEventListener("Socket_" + param1,param2);
         if(param3 != null)
         {
            getEventDispathcer().removeEventListener("SocketError_" + param1,param3);
         }
      }
      
      public static function hasCmdListener(param1:uint) : Boolean
      {
         return getEventDispathcer().hasEventListener("Socket_" + param1);
      }
      
      public static function dispatchCmd(param1:uint, param2:Object = null) : void
      {
         getEventDispathcer().dispatchEvent(new EventTaomee("Socket_" + param1,param2));
      }
      
      public static function dispatchError(param1:uint, param2:Object = null) : void
      {
         getEventDispathcer().dispatchEvent(new EventTaomee("SocketError_" + param1,param2));
      }
      
      private function initialize() : void
      {
         this._cmdSocktDic[LoginCmd.CMD_GET_AUTHCODE] = GetAuthCodeProtocol;
         this._cmdSocktDic[LoginCmd.CMD_LOGIN] = LoginProtocol;
         this._cmdSocktDic[LoginCmd.CMD_GET_GOOD_SERVER_LIST] = GetGoodServerListProtocol;
         this._cmdSocktDic[LoginCmd.CMD_GET_SERVER_LIST] = GetServerListProtocol;
         this._cmdSocktDic[LoginCmd.CMD_CREATE_MOLE] = CreateMoleProtocol;
         this._errSocketResultDic[0] = "线路繁忙，请耐心等待";
         this._errSocketResultDic[5011] = "　　现在是关园时间！";
         this._errSocketResultDic[5014] = "\r你的帐号将被封停三十天!";
         this._errSocketResultDic[5013] = "\r你的帐号将被封停十四天!";
         this._errSocketResultDic[5012] = "\r你的帐号将被封停七天";
         this._errSocketResultDic[5008] = "\r协议不对";
         this._errSocketResultDic[5001] = "该账号未完成身份证实名认证或为未成年人账号受防沉迷限制，请前往account.61.com或kf.61.com查询！";
         this._errSocketResultDic[5005] = "\r帐号错误。";
         this._errSocketResultDic[5010] = "\r你输入的昵称不合法";
         this._errSocketResultDic[5009] = "你输入的密码错误次数太多\r请稍候再试。";
         this._errSocketResultDic[5006] = "你的帐号已经被永久封停 \r将无法登陆摩尔庄园。";
         this._errSocketResultDic[5007] = "系统错误，账号受限或正处在封停状态中，暂时无法登陆摩尔庄园。";
         this._errSocketResultDic[5003] = "\r帐号与密码不符请再试一次吧！";
         this._errSocketResultDic[5004] = "您的帐号没有激活\n请查收邮件激活帐号！";
         this._errSocketResultDic[5002] = "因长时间未登陆，我们暂时冻结了您的帐号,详情请联系kf.61.com";
         this._tempBuffer = new ByteArray();
         this._chunkBuffer = new ByteArray();
      }
      
      public function get isConnected() : Boolean
      {
         return Boolean(this._socket) && Boolean(this._socket.connected);
      }
      
      private function swapLoginIP() : void
      {
         if(this._ipIdx < 2)
         {
            this.setHostPort(this.IP_LIST[this._ipIdx],1863);
            ++this._ipIdx;
         }
         else
         {
            LoginAlert.show(LoginAlert.SYS_ERROR,"可能服务器在维护！",LoginAlert.RESET_LOGIN_AN,[onRefreshPage]);
            LoginDebug.inst.sendError("[S6: Login] 所有连接都失败了！！！很严重");
         }
      }
      
      public function setHostPort(param1:String, param2:uint) : void
      {
         this._host = param1;
         this._port = param2;
      }
      
      public function connect(param1:String, param2:uint) : void
      {
         if(this.isConnected == false)
         {
            LoginDebug.inst.write("登录服务器----> IP:" + this._host + "   Port:" + this._port);
            this.close();
            this._socket = new Socket();
            this._socket.addEventListener(Event.CONNECT,this.onConnectSuccess);
            this._socket.addEventListener(Event.CLOSE,this.onConnectionClose);
            this._socket.addEventListener(IOErrorEvent.IO_ERROR,this.onConnectIoError);
            this._socket.addEventListener(ProgressEvent.SOCKET_DATA,this.onSocketData);
            this._socket.addEventListener(SecurityErrorEvent.SECURITY_ERROR,this.onSocketSecurityError);
            this._socket.connect(param1,param2);
         }
      }
      
      private function onConnectSuccess(param1:Event) : void
      {
         LoginDebug.inst.write("登录服务器连接成功！IP:" + this._host + "   Port:" + this._port);
         if(this.isConnected)
         {
            this.dispatchEvent(new Event(OnSocketConnected));
            if(this._oldData)
            {
               this.send(this._oldData);
               this._oldData = null;
            }
         }
      }
      
      private function onConnectionClose(param1:Event) : void
      {
         LoginDebug.inst.write("连接关闭！");
      }
      
      private function onConnectIoError(param1:IOErrorEvent) : void
      {
         LoginDebug.inst.sendError("[S5: Socket SB E=IO错误具体原因] Svr=" + this._host + ":" + this._port);
         this.swapLoginIP();
      }
      
      private function onSocketSecurityError(param1:SecurityErrorEvent) : void
      {
         LoginDebug.inst.sendError("[S4: Socket SB E=安全沙箱错误具体原因] Svr=" + this._host + ":" + this._port);
         this.swapLoginIP();
      }
      
      private function onSocketData(param1:ProgressEvent) : void
      {
         var _loc4_:int = 0;
         var _loc5_:LoginResPkt = null;
         var _loc6_:String = null;
         var _loc7_:Class = null;
         var _loc8_:Object = null;
         this._chunkBuffer.position = 0;
         this._chunkBuffer.length = 0;
         this._chunkBuffer = new ByteArray();
         if(this._tempBuffer.length > 0)
         {
            this._tempBuffer.position = 0;
            this._tempBuffer.readBytes(this._chunkBuffer,0,this._tempBuffer.length);
            this._tempBuffer.position = 0;
            this._tempBuffer.length = 0;
            this._tempBuffer = new ByteArray();
         }
         this._socket.readBytes(this._chunkBuffer,this._chunkBuffer.length,this._socket.bytesAvailable);
         this._chunkBuffer.position = 0;
         var _loc2_:int = int(this._chunkBuffer.length);
         var _loc3_:int = 0;
         while(_loc2_ > _loc3_)
         {
            if(this._chunkBuffer.bytesAvailable > this.MSG_FIRST_TOKEN_LEN)
            {
               _loc4_ = this._chunkBuffer.readUnsignedInt() - this.MSG_FIRST_TOKEN_LEN;
               if(_loc4_ > this._chunkBuffer.bytesAvailable)
               {
                  this._chunkBuffer.position -= this.MSG_FIRST_TOKEN_LEN;
                  this._chunkBuffer.readBytes(this._tempBuffer,0,this._chunkBuffer.bytesAvailable);
               }
               else
               {
                  this._chunkBuffer.position -= this.MSG_FIRST_TOKEN_LEN;
                  _loc5_ = new LoginResPkt(this._chunkBuffer);
                  if(_loc5_.errorID > 0)
                  {
                     if(_loc5_.errorID != 5005 || _loc5_.cmdID == LoginCmd.CMD_LOGIN)
                     {
                        _loc6_ = this._errSocketResultDic[_loc5_.errorID];
                        if(_loc6_)
                        {
                           LoginAlert.show(LoginAlert.SYS_ERROR,_loc6_,LoginAlert.GOT_AN);
                        }
                     }
                     LoginDebug.inst.write("错误码--->CmdID:" + _loc5_.cmdID + "-->ErrorID:" + _loc5_.errorID + _loc6_);
                     dispatchError(_loc5_.cmdID,_loc5_);
                  }
                  else
                  {
                     _loc7_ = this._cmdSocktDic[_loc5_.cmdID];
                     if(_loc7_)
                     {
                        _loc8_ = new _loc7_(_loc5_);
                        if(_loc5_.cmdID == LoginCmd.CMD_LOGIN)
                        {
                           TongjiUtil.sendTongji(3,_loc5_.userID.toString());
                           TongjiUtil.nowUserId = _loc5_.userID;
                        }
                        else if(_loc5_.cmdID == LoginCmd.CMD_GET_GOOD_SERVER_LIST)
                        {
                           TongjiUtil.sendTongji(5,_loc5_.userID.toString());
                        }
                        dispatchCmd(_loc5_.cmdID,_loc8_);
                        LoginDebug.inst.write("LoginSocket 收到：UserID:" + _loc5_.userID + "    CmdID:" + _loc5_.cmdID);
                     }
                     else
                     {
                        LoginDebug.inst.write("login socket 收到:" + _loc5_.cmdID + " 没有配置解包方法");
                     }
                  }
                  _loc3_ = this._chunkBuffer.position - 1;
                  if(--this._queueCount == 0)
                  {
                     this.close();
                  }
               }
            }
            else
            {
               this._chunkBuffer.readBytes(this._tempBuffer,0,this._chunkBuffer.bytesAvailable);
            }
            _loc3_++;
         }
         if(Boolean(this._loading_mc) && Boolean(this._loading_mc.parent))
         {
            this._loading_mc.parent.removeChild(this._loading_mc);
         }
         clearTimeout(this._waitSocketTimeID);
      }
      
      public function send(param1:ByteArray) : void
      {
         if(this.isConnected == true)
         {
            ++this._queueCount;
            this._socket.writeBytes(param1);
            this._socket.flush();
         }
         else
         {
            this._oldData = param1;
            if(Boolean(this._host) && Boolean(this._port))
            {
               this.connect(this._host,this._port);
            }
         }
         this.showLoading();
      }
      
      private function showLoading() : void
      {
         Login.inst.addChild(this._loading_mc);
         clearTimeout(this._waitSocketTimeID);
         this._waitSocketTimeID = setTimeout(function():void
         {
            close();
            DisplayUtil.removeForParent(_loading_mc,false);
            swapLoginIP();
         },5000);
      }
      
      public function close() : void
      {
         if(this.isConnected == true && Boolean(this._socket))
         {
            this._socket.removeEventListener(Event.CONNECT,this.onConnectSuccess);
            this._socket.removeEventListener(Event.CLOSE,this.onConnectionClose);
            this._socket.removeEventListener(IOErrorEvent.IO_ERROR,this.onConnectIoError);
            this._socket.removeEventListener(ProgressEvent.SOCKET_DATA,this.onSocketData);
            this._socket.removeEventListener(SecurityErrorEvent.SECURITY_ERROR,this.onSocketSecurityError);
            this._socket.close();
            this._socket = null;
            LoginDebug.inst.write("收到包后，主动断开！");
         }
      }
      
      public function destroy() : void
      {
         _instance = null;
         this.close();
      }
   }
}

