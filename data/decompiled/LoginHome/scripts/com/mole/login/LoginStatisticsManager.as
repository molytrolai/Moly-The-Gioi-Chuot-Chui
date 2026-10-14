package com.mole.login
{
   import com.mole.login.config.*;
   import com.mole.login.info.StatisticsInfo;
   import org.taomee.stat.*;
   
   public class LoginStatisticsManager
   {
      
      initialize();
      
      public function LoginStatisticsManager()
      {
         super();
      }
      
      private static function initialize() : void
      {
         StatisticsManager.setup(1);
      }
      
      public static function send(param1:uint) : void
      {
         var _loc2_:StatisticsInfo = LoginStatisticsConfig.inst.getStatisInfo(param1);
         var _loc3_:String = _loc2_.stid;
         var _loc4_:String = _loc2_.sstid;
         var _loc5_:String = _loc2_.item;
         StatisticsManager.sendHttpStat(_loc3_,_loc4_,_loc5_ ? null : _loc5_);
      }
   }
}

