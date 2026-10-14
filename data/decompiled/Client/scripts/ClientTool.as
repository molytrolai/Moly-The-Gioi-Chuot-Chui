package
{
   import flash.display.DisplayObjectContainer;
   import flash.display.MovieClip;
   import flash.external.ExternalInterface;
   import flash.utils.ByteArray;
   import flash.utils.Dictionary;
   import org.taomee.stat.StatisticsManager;
   
   public class ClientTool
   {
      
      private static var _inst:ClientTool;
      
      public static const STAGE_WIDTH:uint = 960;
      
      public static const STAGE_HEIGHT:uint = 560;
      
      private const statistics:Class = ClientTool_statistics;
      
      private var _serXml:XML;
      
      private var _nameHash:Dictionary;
      
      public function ClientTool()
      {
         var nameXml:XML = null;
         super();
         this._nameHash = new Dictionary();
         var nameListXML:XML = XML(new this.statistics());
         for each(nameXml in nameListXML.children())
         {
            this._nameHash[uint(nameXml.@id)] = new StatisticsInfo(nameXml);
         }
      }
      
      public static function get inst() : ClientTool
      {
         if(_inst == null)
         {
            _inst = new ClientTool();
            StatisticsManager.setup(1);
         }
         return _inst;
      }
      
      public static function stopAllMovieClip(dis:DisplayObjectContainer, frame:uint = 0) : void
      {
         var mc:MovieClip = null;
         var child:DisplayObjectContainer = null;
         var len:uint = 0;
         var i:uint = 0;
         if(Boolean(dis))
         {
            mc = dis as MovieClip;
            if(Boolean(mc))
            {
               if(frame > 0)
               {
                  mc.gotoAndStop(frame);
               }
               else
               {
                  mc.stop();
               }
            }
            len = uint(dis.numChildren);
            i = 0;
            while(i < len)
            {
               child = dis.getChildAt(i) as DisplayObjectContainer;
               if(child != null)
               {
                  stopAllMovieClip(child,frame);
               }
               i++;
            }
         }
      }
      
      public static function removeAllChild(dis:DisplayObjectContainer) : void
      {
         var child:DisplayObjectContainer = null;
         if(Boolean(dis))
         {
            while(dis.numChildren > 0)
            {
               child = dis.removeChildAt(0) as DisplayObjectContainer;
               if(child != null)
               {
                  stopAllMovieClip(child);
                  child = null;
               }
            }
         }
      }
      
      public static function get loginSession() : Object
      {
         var loginObj:Object = null;
         var session:ByteArray = null;
         var byteArr:ByteArray = get_URL_Session();
         if(Boolean(byteArr))
         {
            loginObj = new Object();
            byteArr.position = 0;
            loginObj.userID = byteArr.readUnsignedInt();
            session = new ByteArray();
            byteArr.readBytes(session);
            loginObj.session = session;
            return loginObj;
         }
         return null;
      }
      
      public static function get_URL_Session() : ByteArray
      {
         if(!ExternalInterface.available)
         {
            return null;
         }
         var str:String = ExternalInterface.call("get_sid");
         if(Boolean(str))
         {
            return S2B(str);
         }
         return null;
      }
      
      public static function S2B(s:String) : ByteArray
      {
         var b:ByteArray = new ByteArray();
         var l:uint = uint(s.length);
         if(l == 0 || Boolean(l % 2))
         {
            return null;
         }
         var i:uint = 0;
         while(i < l)
         {
            b.writeByte(parseInt(s.substr(i,2),16));
            i += 2;
         }
         b.position = 0;
         return b;
      }
      
      public function getStatisInfo(id:uint) : StatisticsInfo
      {
         return this._nameHash[id];
      }
      
      public function send(id:uint) : void
      {
         var statisticsInfo:StatisticsInfo = this.getStatisInfo(id);
         StatisticsManager.sendHttpStat(statisticsInfo.stid,statisticsInfo.sstid,statisticsInfo.item);
      }
   }
}

class StatisticsInfo
{
   
   private var _id:uint;
   
   private var _stid:String;
   
   private var _sstid:String;
   
   private var _item:String;
   
   public function StatisticsInfo(xml:XML)
   {
      super();
      this._id = xml.@id;
      this._stid = xml.@mainName;
      this._sstid = xml.@partName;
      this._item = xml.@staticsKey;
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
