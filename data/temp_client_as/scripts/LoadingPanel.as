package
{
   import flash.display.Sprite;
   import flash.text.TextField;
   
   public class LoadingPanel extends Sprite
   {
      
      private var _loading_mc:Sprite;
      
      private var _loadingBar:Sprite;
      
      private var _loading_txt:TextField;
      
      private var _desc_txt:TextField;
      
      public function LoadingPanel(loading_mc:Sprite)
      {
         super();
         this._loading_mc = loading_mc;
         this._loadingBar = this._loading_mc["loadingbar"];
         this._loading_txt = this._loading_mc["perNum"];
         this._desc_txt = this._loading_mc["tip_text"];
         this.hide();
      }
      
      public function show() : void
      {
         this.setRate(0);
         this._loading_mc["start"]();
         addChild(this._loading_mc);
      }
      
      public function hide() : void
      {
         if(Boolean(this._loading_mc))
         {
            this._loading_mc["destroy"]();
            if(Boolean(this._loading_mc.parent))
            {
               this._loading_mc.parent.removeChild(this._loading_mc);
            }
         }
      }
      
      public function setRate(rate:Number) : void
      {
         this._loadingBar.scaleX = rate;
         this._loading_txt.text = Math.round(rate * 100).toString() + "%";
      }
      
      public function setDesc(desc:String) : void
      {
         this._desc_txt.text = desc;
      }
      
      public function destroy() : void
      {
         ClientTool.removeAllChild(this);
         this.hide();
      }
   }
}

