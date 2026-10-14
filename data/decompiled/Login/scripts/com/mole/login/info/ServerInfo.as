package com.mole.login.info
{
   import com.mole.login.LoginServerConfig;
   import flash.utils.IDataInput;
   
   public class ServerInfo
   {
      
      private var _id:uint;
      
      private var _name:String;
      
      private var _userCount:uint;
      
      private var _ip:String;
      
      private var _port:uint;
      
      private var _friends:uint;
      
      private var _flag:uint;
      
      public function ServerInfo()
      {
         super();
      }
      
      public function initData(param1:IDataInput) : void
      {
         this._id = param1.readUnsignedInt();
         this._name = LoginServerConfig.inst.getServerName(this._id);
         this._userCount = param1.readUnsignedInt();
         this._ip = param1.readUTFBytes(16);
         this._port = param1.readUnsignedShort();
         this._friends = param1.readUnsignedInt();
      }
      
      public function get flag() : uint
      {
         return this._flag;
      }
      
      public function set flag(param1:uint) : void
      {
         this._flag = param1;
      }
      
      public function get id() : uint
      {
         return this._id;
      }
      
      public function get userCount() : uint
      {
         return this._userCount;
      }
      
      public function get ip() : String
      {
         return this._ip;
      }
      
      public function get port() : uint
      {
         return this._port;
      }
      
      public function get friends() : uint
      {
         return this._friends;
      }
      
      public function get name() : String
      {
         return this._name;
      }
   }
}

