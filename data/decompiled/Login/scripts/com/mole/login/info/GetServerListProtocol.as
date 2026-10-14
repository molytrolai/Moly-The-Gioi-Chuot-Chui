package com.mole.login.info
{
   import com.mole.login.LoginData;
   import com.mole.login.net.LoginResPkt;
   import flash.utils.ByteArray;
   
   public class GetServerListProtocol
   {
      
      private var _serverList:Array;
      
      public function GetServerListProtocol(param1:LoginResPkt)
      {
         var _loc4_:ServerInfo = null;
         super();
         this._serverList = new Array();
         var _loc2_:ByteArray = param1.getBody();
         var _loc3_:int = int(_loc2_.readUnsignedInt());
         var _loc5_:int = 0;
         while(_loc5_ < _loc3_)
         {
            _loc4_ = new ServerInfo();
            _loc4_.initData(_loc2_);
            if(_loc4_.id > 0)
            {
               if(_loc5_ == 0)
               {
                  _loc4_.flag = 1;
               }
               this._serverList.push(_loc4_);
            }
            _loc5_++;
         }
         LoginData.serverList = this._serverList;
      }
      
      public function get serverList() : Array
      {
         return this._serverList;
      }
   }
}

