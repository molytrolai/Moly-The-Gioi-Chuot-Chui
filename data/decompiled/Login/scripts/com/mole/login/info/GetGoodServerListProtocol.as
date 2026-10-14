package com.mole.login.info
{
   import com.mole.login.*;
   import com.mole.login.net.LoginResPkt;
   import com.mole.login.utils.*;
   import flash.net.SharedObject;
   import flash.utils.ByteArray;
   
   public class GetGoodServerListProtocol
   {
      
      private var _serverList:Array;
      
      private var _friendList:Array;
      
      private var _maxServerID:uint;
      
      private var _isVip:Boolean;
      
      public function GetGoodServerListProtocol(param1:LoginResPkt)
      {
         var _loc2_:ByteArray;
         var _loc3_:int;
         var _loc5_:int;
         var _loc6_:int;
         var _loc7_:int;
         var _loc8_:SharedObject;
         var _loc4_:ServerInfo = null;
         var _loc9_:Object = null;
         super();
         this._serverList = new Array();
         _loc2_ = param1.getBody();
         _loc3_ = int(_loc2_.readUnsignedInt());
         _loc5_ = 0;
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
         this._maxServerID = LoginData.maxServerId = _loc2_.readUnsignedInt();
         this._isVip = LoginData.isVip = Boolean(_loc2_.readUnsignedInt());
         this._friendList = new Array();
         _loc6_ = int(_loc2_.readUnsignedInt());
         _loc7_ = 0;
         while(_loc7_ < _loc6_)
         {
            _loc9_ = new Object();
            _loc9_.friend = _loc2_.readUnsignedInt();
            _loc9_.time = _loc2_.readUnsignedInt();
            this._friendList.push(_loc9_);
            _loc7_++;
         }
         LoginData.friendList = this._friendList;
         _loc8_ = MoleSharedObject.getMoleData(LoginData.userID);
         _loc8_.data.ServerFriendsList = this._friendList;
         _loc8_.data.FriendsList = this._friendList;
         try
         {
            _loc8_.flush();
         }
         catch(e:Error)
         {
         }
      }
      
      public function get serverList() : Array
      {
         return this._serverList;
      }
      
      public function get friendList() : Array
      {
         return this._friendList;
      }
      
      public function get maxServerID() : uint
      {
         return this._maxServerID;
      }
      
      public function get isVip() : Boolean
      {
         return this._isVip;
      }
   }
}

