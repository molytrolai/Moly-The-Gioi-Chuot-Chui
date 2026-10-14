package com.mole.login.info
{
   public class StatisticsInfo
   {
      
      private var _id:uint;
      
      private var _stid:String;
      
      private var _sstid:String;
      
      private var _item:String;
      
      public function StatisticsInfo(param1:XML)
      {
         super();
         this._id = param1.@id;
         this._stid = param1.@mainName;
         this._sstid = param1.@partName;
         this._item = param1.@staticsKey;
      }
      
      public function get id() : uint
      {
         return this._id;
      }
      
      public function get stid() : String
      {
         return this._stid;
      }
      
      public function get sstid() : String
      {
         return this._sstid;
      }
      
      public function get item() : String
      {
         return this._item;
      }
   }
}

