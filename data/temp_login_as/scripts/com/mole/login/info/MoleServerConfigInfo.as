package com.mole.login.info
{
   public class MoleServerConfigInfo
   {
      
      private var _moleUrl:String;
      
      private var _errorUrl:String;
      
      private var _houseUrl:String;
      
      private var _allVersion:String;
      
      private var _regVersion:String;
      
      private var _indexVersion:String;
      
      private var _uiVersion:String;
      
      private var _mapVersion:String;
      
      private var _moduleVersion:String;
      
      public function MoleServerConfigInfo(param1:XML)
      {
         super();
         this._moleUrl = param1.@MOUrl;
         this._errorUrl = param1.@ErrorWeb;
         this._houseUrl = param1.@HouseWeb;
         this._allVersion = param1.@allversion;
         this._regVersion = param1.@regversion;
         this._indexVersion = param1.@indexversion;
         this._uiVersion = param1.@uiversion;
         this._mapVersion = param1.@mapversion;
         this._moduleVersion = param1.@moduleversion;
      }
      
      public function get moleUrl() : String
      {
         return this._moleUrl;
      }
      
      public function get errorUrl() : String
      {
         return this._errorUrl;
      }
      
      public function get houseUrl() : String
      {
         return this._houseUrl;
      }
      
      public function get allVersion() : String
      {
         return this._allVersion;
      }
      
      public function get regVersion() : String
      {
         return this._regVersion;
      }
      
      public function get indexVersion() : String
      {
         return this._indexVersion;
      }
      
      public function get uiVersion() : String
      {
         return this._uiVersion;
      }
      
      public function get mapVersion() : String
      {
         return this._mapVersion;
      }
      
      public function get moduleVersion() : String
      {
         return this._moduleVersion;
      }
   }
}

