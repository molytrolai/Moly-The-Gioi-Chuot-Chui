package com.mole.login.info
{
   import com.mole.login.LoginData;
   import com.mole.login.net.LoginResPkt;
   import flash.display.Loader;
   import flash.utils.ByteArray;
   
   public class LoginProtocol
   {
      
      private var _flag:uint;
      
      private var _codeID:ByteArray;
      
      private var _picLoader:Loader;
      
      private var _session:ByteArray;
      
      public function LoginProtocol(param1:LoginResPkt)
      {
         var _loc3_:ByteArray = null;
         var _loc4_:uint = 0;
         var _loc5_:Object = null;
         super();
         var _loc2_:ByteArray = param1.getBody();
         LoginData.userID = param1.userID;
         this._flag = _loc2_.readUnsignedInt();
         if(this._flag > 0)
         {
            this._codeID = new ByteArray();
            _loc3_ = new ByteArray();
            _loc2_.readBytes(this._codeID,0,16);
            _loc4_ = _loc2_.readUnsignedInt();
            _loc2_.readBytes(_loc3_,0,_loc4_);
            this._picLoader = new Loader();
            this._picLoader.loadBytes(_loc3_);
            _loc5_ = new Object();
         }
         else
         {
            LoginData.session = this._session = new ByteArray();
            _loc2_.readBytes(this._session,0,16);
         }
      }
      
      public function get codeID() : ByteArray
      {
         return this._codeID;
      }
      
      public function get picLoader() : Loader
      {
         return this._picLoader;
      }
      
      public function get flag() : uint
      {
         return this._flag;
      }
      
      public function get session() : ByteArray
      {
         return this._session;
      }
   }
}

