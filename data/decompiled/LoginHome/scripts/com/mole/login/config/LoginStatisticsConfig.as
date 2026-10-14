package com.mole.login.config
{
   import com.mole.login.info.*;
   import flash.utils.*;
   
   public class LoginStatisticsConfig
   {
      
      private static var _inst:LoginStatisticsConfig;
      
      private const statistics:Class = LoginStatisticsConfig_statistics;
      
      private var _serXml:XML;
      
      private var _nameHash:Dictionary;
      
      public function LoginStatisticsConfig()
      {
         var _loc2_:XML = null;
         super();
         this._nameHash = new Dictionary();
         var _loc1_:XML = XML(new this.statistics());
         for each(_loc2_ in _loc1_.children())
         {
            this._nameHash[uint(_loc2_.@id)] = new StatisticsInfo(_loc2_);
         }
      }
      
      public static function get inst() : LoginStatisticsConfig
      {
         if(_inst == null)
         {
            _inst = new LoginStatisticsConfig();
         }
         return _inst;
      }
      
      public function getStatisInfo(param1:uint) : StatisticsInfo
      {
         return this._nameHash[param1];
      }
   }
}

