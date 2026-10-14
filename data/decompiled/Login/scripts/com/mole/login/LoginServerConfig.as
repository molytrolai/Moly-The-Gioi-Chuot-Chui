package com.mole.login
{
   import com.mole.login.info.*;
   import flash.utils.*;
   
   public class LoginServerConfig
   {
      
      private static var _inst:LoginServerConfig;
      
      private const ServerName:Class = LoginServerConfig_ServerName;
      
      private var _serXml:XML;
      
      private var _moleServerConfig:MoleServerConfigInfo;
      
      private var _emailIP:IPInfo;
      
      private var _idIP:IPInfo;
      
      private var _regIP:IPInfo;
      
      private var _nameHash:Dictionary;
      
      public function LoginServerConfig()
      {
         var _loc2_:XML = null;
         super();
         this._nameHash = new Dictionary();
         var _loc1_:XML = XML(new this.ServerName());
         for each(_loc2_ in _loc1_.children())
         {
            this._nameHash[uint(_loc2_.@ID)] = String(_loc2_.@Name);
         }
      }
      
      public static function get inst() : LoginServerConfig
      {
         if(_inst == null)
         {
            _inst = new LoginServerConfig();
         }
         return _inst;
      }
      
      public function initServerXml(param1:XML) : void
      {
         this._serXml = param1;
         this._moleServerConfig = new MoleServerConfigInfo(this._serXml.taomee[0]);
         this._idIP = new IPInfo(this._serXml.DirSer[0]);
      }
      
      public function getServerName(param1:uint) : String
      {
         return this._nameHash[param1];
      }
      
      public function get moleServerConfig() : MoleServerConfigInfo
      {
         return this._moleServerConfig;
      }
      
      public function get emailIP() : IPInfo
      {
         return this._emailIP;
      }
      
      public function get idIP() : IPInfo
      {
         return this._idIP;
      }
      
      public function get regIP() : IPInfo
      {
         return this._regIP;
      }
      
      public function get serXml() : XML
      {
         return this._serXml;
      }
      
      public function get nameDict() : Dictionary
      {
         var _loc2_:Object = null;
         var _loc1_:Dictionary = new Dictionary();
         for(_loc2_ in this._nameHash)
         {
            _loc1_["ID_" + _loc2_] = this._nameHash[_loc2_];
         }
         return _loc1_;
      }
   }
}

