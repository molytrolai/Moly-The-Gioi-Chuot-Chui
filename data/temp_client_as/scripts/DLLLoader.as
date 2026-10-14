package
{
   import com.taomee.plugins.versionManager.TaomeeVersionManager;
   import flash.display.Loader;
   import flash.display.LoaderInfo;
   import flash.events.Event;
   import flash.events.EventDispatcher;
   import flash.events.IOErrorEvent;
   import flash.events.ProgressEvent;
   import flash.net.URLLoader;
   import flash.system.ApplicationDomain;
   import flash.system.LoaderContext;
   import flash.utils.ByteArray;
   
   public class DLLLoader extends EventDispatcher
   {
      
      public static var beanData:XML;
      
      public static const LOAD_DLL_SUCC:String = "loadDllSucc";
      
      public static const LOAD_DLL_ERROR:String = "loadDllError";
      
      public static const EXT_NODE_NAME:String = "ext";
      
      public static const BEAN_NODE_NAME:String = "beans";
      
      public static const XML_PATH:String = "resource/xml/ext.xml";
      
      private var _dllArrayByte:ByteArray;
      
      private var _dllTotal:uint;
      
      private var _debug:Boolean = false;
      
      private var _rate:Number;
      
      private var _loadList:Array;
      
      private var _isSucc:Boolean;
      
      public function DLLLoader()
      {
         super();
         this._isSucc = false;
         var urlloader:URLLoader = new URLLoader();
         urlloader.addEventListener(Event.COMPLETE,this.onConfigLoadSucc);
         urlloader.addEventListener(IOErrorEvent.IO_ERROR,this.onConfigLoadError);
         urlloader.load(TaomeeVersionManager.getInstance().getURLRequest(XML_PATH));
      }
      
      private function onConfigLoadError(e:IOErrorEvent) : void
      {
         URLLoader(e.currentTarget).removeEventListener(Event.COMPLETE,this.onConfigLoadSucc);
         URLLoader(e.currentTarget).removeEventListener(IOErrorEvent.IO_ERROR,this.onConfigLoadError);
         dispatchEvent(new Event(LOAD_DLL_ERROR));
      }
      
      private function onConfigLoadSucc(event:Event) : void
      {
         var name:String = null;
         var path:String = null;
         var version:String = null;
         var i:XML = null;
         URLLoader(event.currentTarget).removeEventListener(Event.COMPLETE,this.onConfigLoadSucc);
         URLLoader(event.currentTarget).removeEventListener(IOErrorEvent.IO_ERROR,this.onConfigLoadError);
         var xmlData:XML = new XML(event.target.data);
         this._debug = parseInt(xmlData.@debug) > 0;
         beanData = xmlData.elements(BEAN_NODE_NAME)[0];
         this._dllTotal = 0;
         var dllArray:Array = new Array();
         this._loadList = new Array();
         for each(i in xmlData[EXT_NODE_NAME].elements())
         {
            name = i.@name;
            path = i.@path;
            version = i.@ver;
            ++this._dllTotal;
            this._loadList.push(path);
            dllArray.push({
               "name":name,
               "path":path,
               "ver":version
            });
         }
         this._dllArrayByte = new ByteArray();
         this._dllArrayByte.writeObject(dllArray);
         this.load();
      }
      
      private function load() : void
      {
         var url:String = this._loadList.shift();
         var loader:Loader = new Loader();
         loader.contentLoaderInfo.addEventListener(Event.COMPLETE,this.onLoadOneDllSucc);
         loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR,this.onLoadOneDllFail);
         loader.contentLoaderInfo.addEventListener(ProgressEvent.PROGRESS,this.onProgress);
         loader.load(TaomeeVersionManager.getInstance().getURLRequest(url),new LoaderContext(false,ApplicationDomain.currentDomain));
      }
      
      private function onProgress(e:ProgressEvent) : void
      {
         var loaderInfo:LoaderInfo = e.currentTarget as LoaderInfo;
         var rate:Number = e.bytesLoaded / e.bytesTotal;
         this._rate = (this._dllTotal - this._loadList.length + rate - 1) / this._dllTotal;
         dispatchEvent(e);
      }
      
      private function onLoadOneDllSucc(e:Event) : void
      {
         var loaderInfo:LoaderInfo = e.currentTarget as LoaderInfo;
         loaderInfo.removeEventListener(Event.COMPLETE,this.onLoadOneDllSucc);
         loaderInfo.removeEventListener(IOErrorEvent.IO_ERROR,this.onLoadOneDllFail);
         loaderInfo.removeEventListener(ProgressEvent.PROGRESS,this.onProgress);
         if(this._loadList.length == 0)
         {
            this._isSucc = true;
            dispatchEvent(new Event(LOAD_DLL_SUCC));
         }
         else
         {
            this.load();
         }
      }
      
      private function onLoadOneDllFail(e:IOErrorEvent) : void
      {
         dispatchEvent(new Event(LOAD_DLL_ERROR));
      }
      
      public function get isSucc() : Boolean
      {
         return this._isSucc;
      }
      
      public function get rate() : Number
      {
         return this._rate;
      }
      
      public function destroy() : void
      {
      }
      
      public function get dllArrayByte() : ByteArray
      {
         return this._dllArrayByte;
      }
      
      public function get debug() : Boolean
      {
         return this._debug;
      }
   }
}

