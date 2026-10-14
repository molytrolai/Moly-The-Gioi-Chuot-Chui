package com.mole.login.info
{
   import com.mole.login.net.*;
   import flash.utils.ByteArray;
   
   public class CreateMoleProtocol
   {
      
      public function CreateMoleProtocol(param1:LoginResPkt)
      {
         super();
         var _loc2_:ByteArray = param1.getBody();
         LoginPktParser.GetRecomServers();
      }
   }
}

