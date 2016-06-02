<style>
#skills_box{ padding:10px;}
.show_box{ min-height:40px; overflow:hidden; border:1px solid #f0f0f0}
.show_box .skill{float:left; margin:8px 3px; padding:0 4px; line-height:20px; border:1px solid #999; -moz-border-radius:2px; -webkit-border-radius:2px; border-radius:2px; background:#ededed;}
.show_box .skill span{ float:right; cursor:pointer; padding-left:3px; border-left:#787878 solid 1px; margin-left:3px;}
.show_box .end_remind{float:left; min-width:20px; width:20px; border:none; outline:none; height:20px; margin:8px 0; line-height:20px; font-size:14px;}
.drop_list{max-height:340px; overflow:auto; border:1px solid #f0f0f0;}
.drop_list .not_skill{ line-height:24px; padding-left:3px; cursor:pointer;}
.drop_list .not_skill:hover{ background:#ededed;}
</style>
<template>
<div id="skills_box" v-on:mouseout.self="modal_hide()" v-on:mouseover="modal_show()">
  <div class="show_box" v-on:click="input_focus($event)">
    <div class="skill" v-for="skill in selected_skills">
      {[skill]}<span v-on:click="delete_skill($index)">X</span>
    </div>
    <input class="end_remind" v-on:keydown="back_delete($event)" v-on:blur="input_blur($event)">
  </div>
  <div class="drop_list" v-show="down_show">
    <div class="not_skill" v-for="skill in not_selected_skills" v-on:click="add_skill($index,$event)">{[skill]}</div>
  </div>
</div>
</template>

<script>
  import $ from 'jquery'
  export default {
    data () {
      return {
        all_skills: 'Tomcat,Zeus,Lighttpd,IIS,Blackberry,Symbian,Palm OS & Web OS,Blackberry,Windows phone,Android,Linux,Mac OS,Apache HTTP Server,Nginx,Mtk,IOS ,Windows,Websphere Application Server,Weblogic Server,Tong Web,Apusic Application Server,Jetty,Resin,Geronimo,Jboss Application Server,MS Access,BerkeleyDB,CouchDB,HANA,HBASE,IBM DB2,Informix,Microsoft SQL Server,MongoDB,MySQL,NoSQL,Oracle,CakePHP,PostgreSQL,SQLite,Sybase,Teradata,Awt/Swing,C,C++,C#,Eclipse,Eclipse PDE/RCP,Eclipse Plugin Development,Eclipse SWT/JFace,J2SE,Java,COM/COM+,Delphi,MFC,Office开发,PowerBuilder,PowerScript,VBA,VC++,Visual Basic,Visual Basic.NET,Visual Studio,windows-app-development,Winform,linux-app-development,Python,Ruby,Qt,unix-systems-development,ActionScript,Ajax,CSS/CSS3,DIV+CSS,flash,HTML/DHMTL,JSON,ORM,Redis,RESTful,Silverlight,SOAP,SoapUI,twitter-bootstrap,XML,XQuery,XSLT/XPath,Yii Framework,Zend Framework,symfony,smarty,Silex Framework,QCodo,Prado PHP Framework,PHPNuke,PHPfox,Phing,moodle,lithium framework,kohana,Joomla,fusebox,Drupal,CodeIgniter,Hibernate ,iBatis/MyBatis,Java EE , Java Servlet ,ICEfaces ,JBoss Seam,JSF ,JSP,Mockito,Apache Camel,R1 BizFoundation,RMI, Apache Cocoon,Spring Framework,Apache CXF,Apache Tiles,AppFuse,SSH,struts,backbone-js,dojo,ExtJS,limejs,mocha,mootools,prototypejs,qooxdoo, spine-dot-js,jQuery,node.js,JX,KISSY,QWrap,Tangram,Como,Sonic,Chart.js,Zebra,Workless,Junior,Radi,HTML5 Bones,Literally Canvas,Gauge.js,WYSIHTML5,HTML5 Sortable,Lungo.JS,Kendo UI,Jo,52 Framework,G5 Framework,django-framework,flask,Pylons,python-scipy,Scrapy Framework,tastypie,zope,Oracle APEX,perl-catalyst,perl-mojolicious,PerlDancer,Play Framework,Ruby on Rails,Sinatra Framework,Cocoa Touch,iOS-development,iPad,ipad-app-development,iPhone,iphone-app-development, Objective-C,Quartz Composer,Xcode,Bluetooth,Brew,Cocos2d-x,CoffeeScript,HBuilder,HTML5,J2ME,jQTouch,jQueryMobile,PhoneGap, Sencha Touch,TitaniumMobile,Unity3D,WAP,ORMLite,ASP.NET,.NET Compact Framework,.NET Framework,DevExpress,Entity Framework,IdeaBlade DevForce,N2CMS,SharePoint,WCF,WPF,Photoshop,Firework,Coreldraw,illustrator,Animation,Cartoon,Freehand,3D Max,Autocad,Maya,Axure,Mockups,UI Design,PHP',
        not_selected_skills: [],
        current_index: -1,
        down_show: false
      }
    },
    props: ['selected_skills'],
    created () {
      let that = this
      this.init_skill(that)
    },
    methods: {
      init_skill (obj) {
        let skills = obj.all_skills.split(',')
        obj.current_index = obj.selected_skills.length - 1
        let set_selected_skills = new Set(obj.selected_skills)
        let set_not_selected_skills = new Set(skills.filter(x => !set_selected_skills.has(x)))
        obj.not_selected_skills = [...set_not_selected_skills]
      },
      delete_skill (index) {
        let that = this
        that.selected_skills.splice(index, 1)
        that.init_skill(that)
      },
      add_skill (index, event) {
        let that = this
        $(event.target).parent('.drop_list').prev().find('input').focus()
        that.selected_skills.push(that.not_selected_skills[index])
        that.init_skill(that)
      },
      input_focus (event) {
        $(event.target).find('input').css({width: 20})
        $(event.target).find('input').focus()
        this.down_show = true
      },
      input_blur (event) {
        let that = this
        let val = $(event.target).val()
        if (val !== '') {
          that.selected_skills.push(val)
          that.init_skill(that)
          $(event.target).val('')
        }
      },
      back_delete (event) {
        let that = this
        $(event.target).css({width: $(event.target).val().length * 14})
        if ($(event.target).val().length === 0 && event.keyCode === 8) {
          that.delete_skill(that.current_index)
        }
      },
      modal_hide () {
        let that = this
        if (that.down_show) {
          $(document).one('click', (e) => {
            if (e.type === 'click') {
              that.down_show = false
            }
          })
        }
      },
      modal_show () {
        $(document).unbind('click')
      }
    }
  }

</script>
