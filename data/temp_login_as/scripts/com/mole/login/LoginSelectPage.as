package com.mole.login
{
   import com.mole.*;
   import com.mole.login.info.*;
   import com.mole.login.net.*;
   import com.mole.login.type.*;
   import com.mole.login.utils.*;
   import flash.display.*;
   import flash.events.*;
   import flash.geom.*;
   import flash.net.*;
   import flash.ui.*;
   import flash.utils.*;
   
   public class LoginSelectPage extends PageBase
   {
      
      private var _login_btn:SimpleButton;
      
      private var _findPwd_btn:SimpleButton;
      
      private var _modifyPwd_btn:SimpleButton;
      
      private var _protectPwd_btn:SimpleButton;
      
      private var _removeSystem_btn:SimpleButton;
      
      private var _authCode:LoginOneAuthCode;
      
      private var _pwd_mc:Sprite;
      
      private var _rem_pwd:LoginCheckBox;
      
      private var _newLogin_btn:SimpleButton;
      
      private var _clickOneMole:LoginSelectOneMole;
      
      private var _oneVector:Vector.<LoginSelectOneMole>;
      
      private var _container:Sprite;
      
      private const CHARACTER_MAX:uint = 5;
      
      private const ANGLE_INTERVAL:uint = 72;
      
      private const TIME_TOTAL:uint = 500;
      
      private const RADIUS:uint = 480;
      
      private var D_T_R:Number = 0.0174533;
      
      private var _currentIndex:int;
      
      private var _currentTime:uint;
      
      private var _timeElasped:int;
      
      private var _acceleration:Number;
      
      private var _speed:Number;
      
      public function LoginSelectPage()
      {
         var _loc1_:LoginSelectOneMole = null;
         super(new RES_Login_SelectMole());
         _page_mc.x = _page_mc.y = 0;
         _page_mc["bg_mc"].gotoAndStop(1);
         this._removeSystem_btn = _page_mc["removeSystem_btn"];
         this._removeSystem_btn.addEventListener(MouseEvent.CLICK,this.clearOneInfo);
         this._rem_pwd = new LoginCheckBox(_page_mc["rem_pwd"]);
         this._rem_pwd.addEventListener(LoginCheckBox.STATE_CHANGE,this.onRemPwd);
         this._newLogin_btn = _page_mc["newLogin_btn"];
         this._newLogin_btn.addEventListener(MouseEvent.CLICK,this.onNewLogin);
         this._authCode = new LoginOneAuthCode(_page_mc["authCode_mc"],30);
         this._pwd_mc = _page_mc["pwd_mc"];
         this._pwd_mc["pwd_txt"].displayAsPassword = true;
         this._login_btn = _page_mc["login_btn"];
         this._findPwd_btn = _page_mc["findPwd_btn"];
         this._modifyPwd_btn = _page_mc["modifyPwd_btn"];
         this._protectPwd_btn = _page_mc["protectPwd_btn"];
         this._login_btn.y = 492;
         this._pwd_mc.y = 530;
         _page_mc["rem_pwd"].y = 530;
         this._pwd_mc["pwd_txt"].addEventListener(KeyboardEvent.KEY_DOWN,this.onEnterKeyDown);
         this._login_btn.addEventListener(MouseEvent.CLICK,this.onLogin);
         this._findPwd_btn.addEventListener(MouseEvent.CLICK,this.onFindPwd);
         this._modifyPwd_btn.addEventListener(MouseEvent.CLICK,this.onModifyPwd);
         this._protectPwd_btn.addEventListener(MouseEvent.CLICK,this.onProtectPwd);
         LoginSocket.addCmdListener(LoginCmd.CMD_LOGIN,this.onSocketLogin);
         this._container = new Sprite();
         this._oneVector = new Vector.<LoginSelectOneMole>();
         var _loc2_:Array = LoginShared.loginList;
         _loc2_.sortOn("time",Array.NUMERIC);
         var _loc3_:int = 0;
         while(_loc3_ < this.CHARACTER_MAX)
         {
            _loc1_ = new LoginSelectOneMole();
            _loc1_.addEventListener(MouseEvent.CLICK,this.onEnterMole);
            this._oneVector.push(_loc1_);
            this._container.addChild(_loc1_);
            if(_loc2_.length > _loc3_)
            {
               _loc1_.setInfo(_loc2_[_loc2_.length - 1 - _loc3_]);
               if(this._clickOneMole == null)
               {
                  this._clickOneMole = _loc1_;
                  if(this._clickOneMole.info.pwd)
                  {
                     this._pwd_mc["pwd_txt"].text = "**********";
                  }
                  this._rem_pwd.setState(this._clickOneMole.info.remPwd);
               }
            }
            else
            {
               _loc1_.setInfo(null);
            }
            _loc3_ += 1;
         }
         this._container.transform.perspectiveProjection = new PerspectiveProjection();
         this._container.transform.perspectiveProjection.projectionCenter = new Point(420,-150);
         addChild(this._container);
         this.initItemPosition();
      }
      
      private function onRemPwd(param1:EventTaomee) : void
      {
         if(param1.EventObj)
         {
            LoginAlert.show(LoginAlert.NORMAL_WARN,"只有在自己家里上网才能选择，并要牢记帐号和密码哦！",LoginAlert.GOT_AN);
         }
      }
      
      private function checkUserShared(param1:String) : void
      {
         var _loc2_:Object = new Object();
         _loc2_.remID = this._rem_pwd.selected;
         _loc2_.userID = this._clickOneMole.info.userID;
         _loc2_.userCode = this._clickOneMole.node_mc["id_txt"].text;
         if(this._rem_pwd.selected)
         {
            if(param1.length != 32)
            {
               param1 = LoginUtil.upsetPwd(this._pwd_mc["pwd_txt"].text);
            }
            _loc2_.pwd = param1;
         }
         _loc2_.remPwd = this._rem_pwd.selected;
         _loc2_.time = new Date().time;
         LoginShared.addUser(_loc2_);
      }
      
      private function clearOneInfo(param1:Event) : void
      {
         var _str:String;
         var _alt:AlertPanel = null;
         var e:Event = param1;
         _alt = new AlertPanel();
         _alt.x = 480 - _alt.width / 2;
         _alt.y = 280 - _alt.height / 2;
         addChild(_alt);
         _str = "清空本地帐号不会删除帐号内物品！如果小摩尔是在学校、网吧等公共场所上网，建议将本地帐号清空，避免盗号！" + "\r" + "是否清空本地帐号？";
         _alt.setTxt(_str,function():void
         {
            var _loc1_:Array = LoginShared.loginList;
            var _loc2_:uint = 0;
            while(_loc2_ < _loc1_.length)
            {
               LoginShared.removeUser(_loc1_[_loc2_].userID);
               _loc2_++;
            }
            _alt.destory();
            removeChild(_alt);
            LoginShared.loginList = null;
            Login.inst.showPage(2);
         },function():void
         {
            _alt.destory();
            removeChild(_alt);
         });
      }
      
      private function onEnterMole(param1:MouseEvent) : void
      {
         var _loc2_:LoginSelectOneMole = param1.currentTarget as LoginSelectOneMole;
         if(_loc2_.info != null)
         {
            this._clickOneMole = _loc2_;
            if(this._clickOneMole.info != null)
            {
               this._rem_pwd.setState(this._clickOneMole.info.remPwd);
            }
            if(this._clickOneMole.info != null && Boolean(this._clickOneMole.info.pwd))
            {
               this._pwd_mc["pwd_txt"].text = "**********";
            }
            else
            {
               this._pwd_mc["pwd_txt"].text = "";
            }
            this.stage.focus = this._pwd_mc["pwd_txt"];
            if(this._oneVector.indexOf(this._clickOneMole) != this._currentIndex)
            {
               this.rollToPosition(this._oneVector.indexOf(this._clickOneMole));
            }
            return;
         }
      }
      
      private function initItemPosition(param1:int = 0) : void
      {
         var _loc2_:LoginSelectOneMole = null;
         var _loc3_:int = 0;
         this._currentIndex = param1;
         var _loc4_:int = 0;
         while(_loc4_ < this.CHARACTER_MAX)
         {
            _loc2_ = this._oneVector[_loc4_];
            _loc3_ = (_loc4_ - this._currentIndex) * this.ANGLE_INTERVAL;
            if(_loc3_ < 0)
            {
               _loc3_ += 360;
            }
            this.setItemPosition(_loc2_,_loc3_);
            _loc4_ += 1;
         }
         this.sortItemDepth();
      }
      
      private function setItemPosition(param1:LoginSelectOneMole, param2:Number) : void
      {
         var _loc3_:* = this.getCirclePoint(new Point(),param2,this.RADIUS);
         param1.z = this.RADIUS - _loc3_.x;
         param1.x = _loc3_.y;
         param1.angle = param2;
      }
      
      public function getCirclePoint(param1:Point, param2:Number, param3:Number) : Point
      {
         var _loc4_:* = param2 * this.D_T_R;
         return param1.add(new Point(Math.cos(_loc4_) * param3,Math.sin(_loc4_) * param3));
      }
      
      private function sortItemDepth() : void
      {
         var _loc1_:DisplayObject = null;
         var _loc2_:* = this._container.numChildren;
         var _loc3_:Array = new Array();
         var _loc4_:int = 0;
         while(_loc4_ < _loc2_)
         {
            _loc1_ = this._container.getChildAt(_loc4_);
            _loc3_.push(_loc1_);
            _loc4_ += 1;
         }
         _loc3_.sortOn("z",Array.NUMERIC | Array.DESCENDING);
         var _loc5_:int = 0;
         while(_loc5_ < _loc2_)
         {
            this._container.setChildIndex(_loc3_[_loc5_],_loc5_);
            _loc5_ += 1;
         }
      }
      
      private function rollToPosition(param1:int) : void
      {
         var _loc2_:Number = Number(NaN);
         this._currentIndex = (param1 + this.CHARACTER_MAX) % this.CHARACTER_MAX;
         if(!hasEventListener(Event.ENTER_FRAME))
         {
            addEventListener(Event.ENTER_FRAME,this.onEnterFrame);
         }
         var _loc3_:LoginSelectOneMole = this._oneVector[this._currentIndex];
         if(_loc3_.angle <= 180)
         {
            _loc2_ = -_loc3_.angle;
         }
         else
         {
            _loc2_ = 360 - _loc3_.angle;
         }
         this._currentTime = getTimer();
         this._timeElasped = 0;
         var _loc4_:* = _loc2_ / (1.5 * this.TIME_TOTAL);
         this._speed = _loc4_ * 2;
         this._acceleration = -_loc4_ / this.TIME_TOTAL;
      }
      
      private function onEnterFrame(param1:Event) : void
      {
         var _loc2_:Number = Number(NaN);
         var _loc3_:int = 0;
         var _loc4_:LoginSelectOneMole = null;
         var _loc5_:Number = Number(NaN);
         var _loc6_:* = getTimer() - this._currentTime;
         this._timeElasped += _loc6_;
         this._currentTime += _loc6_;
         if(this._timeElasped > this.TIME_TOTAL)
         {
            this.initItemPosition(this._currentIndex);
            removeEventListener(Event.ENTER_FRAME,this.onEnterFrame);
         }
         else
         {
            _loc2_ = (this._speed * 2 + this._acceleration) * _loc6_ * 0.5;
            this._speed += this._acceleration * _loc6_;
            _loc3_ = 0;
            while(_loc3_ < this.CHARACTER_MAX)
            {
               _loc4_ = this._oneVector[_loc3_];
               _loc5_ = _loc4_.angle + _loc2_;
               _loc5_ = (_loc5_ + 360) % 360;
               this.setItemPosition(_loc4_,_loc5_);
               _loc3_ += 1;
            }
            this.sortItemDepth();
         }
      }
      
      private function onNewLogin(param1:MouseEvent) : void
      {
         Login.inst.showPage(2);
      }
      
      private function onFindPwd(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("http://account.61.com/forget"));
      }
      
      private function onModifyPwd(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("http://account.61.com/change"));
      }
      
      private function onProtectPwd(param1:MouseEvent) : void
      {
         navigateToURL(new URLRequest("http://account.61.com/protect"));
      }
      
      private function onEnterKeyDown(param1:KeyboardEvent) : void
      {
         if(param1.keyCode == Keyboard.ENTER)
         {
            this.onLogin();
         }
      }
      
      public function onLogin(param1:MouseEvent = null) : void
      {
         if(this._clickOneMole == null || this._pwd_mc["pwd_txt"].text.length < 6)
         {
            stage.focus = this._pwd_mc["pwd_txt"];
            LoginAlert.show(LoginAlert.SYS_PROMPT,"密码不能为空且要大于5位！",LoginAlert.GOT_AN);
            return;
         }
         var _loc2_:Object = LoginUtil.loginSession;
         if(Boolean(_loc2_) && _loc2_.userID == uint(this._clickOneMole.node_mc["id_txt"].text))
         {
            LoginData.userID = _loc2_.userID;
            LoginDebug.inst.write("UserID---->" + LoginData.userID);
            this.enterGameConfrim();
         }
         else
         {
            this.checkLogin();
         }
      }
      
      private function checkLogin(param1:MouseEvent = null) : void
      {
         if(this._clickOneMole == null || this._pwd_mc["pwd_txt"].text.length < 6)
         {
            return;
         }
         var _loc2_:String = this._clickOneMole.node_mc["id_txt"].text;
         var _loc3_:String = this._pwd_mc["pwd_txt"].text;
         if(_loc3_ == "**********")
         {
            _loc3_ = this._clickOneMole.info.pwd;
         }
         if(Login.inst.getAccountState(_loc2_) > 0)
         {
            if(Boolean(_loc3_) && _loc3_.length >= 6)
            {
               this.sendLogin(_loc2_,_loc3_);
            }
            else
            {
               LoginAlert.show(LoginAlert.SYS_PROMPT,"密码不能为空且要大于5位！",LoginAlert.GOT_AN);
            }
         }
         else
         {
            LoginAlert.show(LoginAlert.SYS_PROMPT,"帐号错误。",LoginAlert.GOT_AN);
         }
      }
      
      private function onSocketLogin(param1:EventTaomee) : void
      {
         var _loc3_:String = null;
         var _loc4_:RegCipher = null;
         var _loc2_:LoginProtocol = param1.EventObj as LoginProtocol;
         if(_loc2_.flag == 0)
         {
            _loc3_ = this._pwd_mc["pwd_txt"].text;
            _loc4_ = new RegCipher();
            if(_loc4_.check(_loc3_))
            {
               LoginAlert.show(LoginAlert.NORMAL_WARN,"你的密码太简单啦！英文+数字更加安全哦！",LoginAlert.MODIFY_PWD_AN | LoginAlert.ENTER_GAME_AN,[this.modifyPwd,this.enterGameConfrim],[[],[]]);
            }
            else
            {
               this.enterGameConfrim();
            }
         }
         else
         {
            if(_loc2_.flag == 1)
            {
               LoginAlert.show(LoginAlert.SYS_ERROR,"密码错误！",LoginAlert.GOT_AN);
            }
            else if(_loc2_.flag == 2)
            {
               LoginAlert.show(LoginAlert.SYS_ERROR,"验证码错误！",LoginAlert.GOT_AN);
            }
            this._authCode.show(_loc2_.codeID,_loc2_.picLoader,false);
            _page_mc["bg_mc"].gotoAndStop(2);
            this._login_btn.y = 448;
            this._pwd_mc.y = 516;
            _page_mc["rem_pwd"].y = 516;
         }
      }
      
      private function enterGameConfrim() : void
      {
         Login.inst.showPage(3);
      }
      
      private function modifyPwd() : void
      {
         navigateToURL(new URLRequest("http://account.61.com/main?goto_url=%2Fchange&referer=%2Fchange"));
      }
      
      private function sendLogin(param1:String, param2:String) : void
      {
         this.checkUserShared(param2);
         if(param2.length == 32)
         {
            param2 = LoginUtil.changeRemenberedPwdPos(param2);
         }
         if(Login.inst.getAccountState(param1) == 1)
         {
            LoginPktParser.IdLogin(uint(param1),param2,this._authCode.authObj);
         }
         else
         {
            LoginPktParser.EmailLogin(param1,param2,this._authCode.authObj);
         }
      }
      
      override public function destroy() : void
      {
         var _loc1_:LoginSelectOneMole = null;
         for each(_loc1_ in this._oneVector)
         {
            _loc1_.removeEventListener(MouseEvent.CLICK,this.onEnterMole);
            _loc1_.destroy();
         }
         this._oneVector = null;
         this._removeSystem_btn.removeEventListener(MouseEvent.CLICK,this.clearOneInfo);
         this._rem_pwd.removeEventListener(LoginCheckBox.STATE_CHANGE,this.onRemPwd);
         this._newLogin_btn.removeEventListener(MouseEvent.CLICK,this.onNewLogin);
         this._login_btn.removeEventListener(MouseEvent.CLICK,this.onLogin);
         this._findPwd_btn.removeEventListener(MouseEvent.CLICK,this.onFindPwd);
         this._modifyPwd_btn.removeEventListener(MouseEvent.CLICK,this.onModifyPwd);
         this._protectPwd_btn.removeEventListener(MouseEvent.CLICK,this.onProtectPwd);
         LoginSocket.removeCmdListener(LoginCmd.CMD_LOGIN,this.onSocketLogin);
         super.destroy();
      }
   }
}

