<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">
<font color=#999AAA >提示：以下是本篇文章正文内容，下面案例可供参考

# 一、分析问题
<font color=#999AAA >我们既然要爬取动漫图片，那么我们就可以直接打开对应的界面优先去查找，看有没有我们想要的数据。
按照常例，我们先打开控制台看一下是否存在接口返回图片相关的数据。
![在这里插入图片描述](https://img-blog.csdnimg.cn/aec17e06a78d4f02bfa13222be3bd960.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA56ia5bCP55m9,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
我们发现没有任何和图片有关的接口，那么我们直接查看当前网页源代码，看是否存在相关的数据。
（图片太大了，放不上来。直观上看发现并没有相关的数据）

此时我们应该如何破局了？？？


<font color=#999AAA >我们先直接找到图片对应的节点
![在这里插入图片描述](https://img-blog.csdnimg.cn/f0cd02968e6f46ee87f21e90fe81b2a7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA56ia5bCP55m9,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
我们在这里可以发现，这里有两个方法：
1.prev_img()
2.next_img()
这两个方法是做什么的呢？
很明显一个是上一张一个是下一张。
此时我想大家都很疑惑，这和图片有什么关系？？
此言差矣，这两个方法和图片有关且存在对图片的操作，我们可以顺藤摸瓜一路找过去啊。
我们先直接在top文件夹下搜索两个中的任意一个即可
![在这里插入图片描述](https://img-blog.csdnimg.cn/b6e51b472e774cf4beff4af15290ba4b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA56ia5bCP55m9,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
找到以后我们直接点进去，以下贴出该js文件代码

```javascript
pages = pages.replace(/\n/g,"");
pages = pages.replace(/\r/g,"|");
var info = eval("(" + pages + ")");
var picArry = info['page_url'].split("|");
var pic_total = info['sum_pages'];

var next_charper = $(".next a").attr("href");
var img_prefix = 'https://images.dmzj.com/';


var prevChapter = $(".pre a").size()>0?'<a class="btm_chapter_btn fl" href="'+$(".pre a").attr("href")+'">上一章节</a>':'';
var nextChapter = $(".next a").size()>0?'<a class="btm_chapter_btn fr" href="'+$(".next a").attr("href")+'">下一章节</a>':'';
var app_html = '<div id="app_manhua" style="width:800px; height:10px; padding:20px; background:#fff; display:block;  margin:20px auto"></div>';

$(".comic_wraCon").after(app_html);

/*
if($.cookie('my')!=null){
    var userId = $.cookie('my').split("|")[0]
}
*/


//竖屏显示图片
function getImg(data){
    for(var i=0; i<data.length; i++){
        $(".comic_wraCon").append($('<a name="page='+(i+1)+'" id="page'+(i+1)+'" onclick="next_pic('+(i+1)+')"></a>')
                          .append($('<img data-original="https://images.dmzj.com/'+data[i]+'">').lazyload({
                            placeholder : "https://static.dmzj.com/ocomic/images/mh-last/lazyload.gif",
                            effect: "fadeIn",
                            threshold:2000
        })).append('<p class="mh_curr_page">'+parseInt(i+1)+'/'+pic_total+'</p>'));
    }
    $("#app_manhua").after('<div class="btmBtnBox">'+prevChapter+nextChapter+'</div>');
    historyCookie(comic_id,sns_sys_id.split("_")[1],1);
}

//getImg(picArry);

function next_pic(index){
    if(index<pic_total){
        location.href = '#page='+(parseInt(index)+1);
    }else{
        if($(".next a").size()>0){
            $(".show").show();
            $(".red_box").show();
        }else{
            openBoxOne();
        }
    }
}

function closeBoxTwo(){
    $(".show").hide();
    $(".red_box").hide();
}
$(".manag>a").click(function(){
    closeBoxTwo();
});

$(".lz_btn").click(function(){
    closeBoxTwo();
});

$(".next_btn").click(function(){
    closeBoxTwo();
    location=next_charper;
});


var img1=new Image();
var img2=new Image();

//横向显示图片
function getImg_land(data){
    if(document.location.hash==false){
        document.location.hash = '@page=1';
        var his_img = 1;
    }else{
        var his_img = document.location.hash.split("=")[1];
    }
    var img_src = img_prefix + data[his_img-1];
    var img = '<img name="page_1" src="'+img_src+'"/>';
    var select_option ='';
    for(var i=0; i<data.length; i++){
        select_option+='<option value="'+img_prefix+data[i]+'">第'+(i+1)+'页</option>';
    }
    var select_h = '<select name="select" id="page_select" onchange="select_page()">'+select_option+'</select>';
    $(".comic_wraCon").append(img);
    $(".comic_wraCon").append('<a class="img_land_prev" onclick="prev_img()"></a><a class="img_land_next" onclick="next_img()"></a>');
    $("#app_manhua").after('<div class="btmBtnBox">'+prevChapter+select_h+nextChapter+'</div>');
    $("#page_select option").eq(his_img-1).attr("selected","selected");
    if(picArry.length > 1) {
        img2.src = img_prefix + picArry[1];
    }
    historyCookie(comic_id,sns_sys_id.split("_")[1],his_img);
}

function prev_img(){
    var cur_img = decodeURI($(".comic_wraCon").find("img").attr("src"));
    for(var i=0; i<picArry.length;i++){
        var img_src = img_prefix+picArry[i];
        if(cur_img==img_src){
            var imgStr = '<img src="'+img_prefix+picArry[i-1]+'"/>';
            if(img_prefix+picArry[i-1]!="https://images.dmzj.com/undefined"){
                $(".comic_wraCon").find("img").remove();
                $(".comic_wraCon").append(imgStr);
                curr_page=parseInt(i);
                historyCookie(comic_id,sns_sys_id.split("_")[1],curr_page);
                $(".comic_wraCon").find("img").load(function(){
                    if($.cookie('pic_style')==1){
                        if($(this).width()>$(window).width()){
                            $(this).css("width",$(window).width()-50+"px")
                        }
                    }
                });
                document.location.hash='@page='+(i);
                $("#page_select option").eq(i-1).attr("selected","selected");
                $("html,body").animate({
                    "scrollTop": $(".comic_wraCon").offset().top
                },0)
            }else{
                if($(".pre a").size()>0){
                    if(confirm("已经是此章节第1页了，要打开上一个章节吗？")==true){
                        location.href = $(".pre a").attr("href");
                    }
                }else{
                    alert("已经是第一个章节了!")
                }
            }
            break
        }
    }
}

function next_img(){
    var obj_img_src =decodeURI($(".comic_wraCon").find("img").attr("src"));
    for(var i=0; i<picArry.length;i++){
        var img_src = img_prefix+picArry[i];
        if(obj_img_src==img_src){
            var imgStr = '<img src="'+img_prefix+picArry[i+1]+'"/>';
            if(img_prefix+picArry[i+1]!="https://images.dmzj.com/undefined"){
                $(".comic_wraCon").find("img").remove();
                $(".comic_wraCon").append(imgStr);
                curr_page=parseInt(i)+2;
                historyCookie(comic_id,sns_sys_id.split("_")[1],curr_page);
                $(".comic_wraCon").find("img").load(function(){
                    if($.cookie('pic_style')==1){
                        if($(this).width()>$(window).width()){
                            $(this).css("width",$(window).width()-50+"px")
                        }
                    }
                });
                document.location.hash='@page='+(i+2);
                if(img_prefix+picArry[i+2]!="https://images.dmzj.com/undefined") {
                    img1.src = img_prefix+picArry[i+2];
                }
                $("#page_select option").eq(i+1).attr("selected","selected");
                $("html,body").animate({
                    "scrollTop": $(".comic_wraCon").offset().top
                },0)
            }else{
                if($(".next a").size()>0){
                    $(".show").show();
                    $(".red_box").show();
                }else{
                    openBoxOne();
                }
            }
            break
        }
    }

}

function select_page(){
    var options=$("#page_select option:selected").val();
    var _index = $("#page_select option:selected").index()+1;
    $(".comic_wraCon").find("img").attr("src",options);
    $(".comic_wraCon").find("img").attr("name","page_"+(_index));
    curr_page =_index;
    historyCookie(comic_id,sns_sys_id.split("_")[1],curr_page);
    document.location.hash = '@page='+_index;
    $("html,body").animate({
        "scrollTop": $(".comic_wraCon").offset().top
    },0)
}



function historyLog(historyJson){
    if($.cookie('my') != null){
        var userId = $.cookie('my').split("|")[0];
        $.ajax({
            type: "get",
            url: "https://interface.dmzj.com/api/record/getRe",
            dataType: "jsonp",
            jsonp: 'callback',
            jsonpCallback: "record_jsonpCallback",
            data: {uid:userId,type:1,st:"comic",json:historyJson},
            success: function (e) {
            }
        });
    }
}

var chapter_id = sns_sys_id.split("_")[1];
var defaul_page = window.location.hash.split("=")[1];


function historyCookie(comic_Id,chapter_id,curr_Page){
    if($.cookie('my') == null){
        return false
    }
    var cookieData = Date.parse(new Date()).toString().substr(0,10);
    if($.cookie("history_Cookie")==undefined){
        var item_obj = {};
        item_obj[comic_Id] = chapter_id;
        item_obj["comicId"] = comic_Id;//漫画id
        item_obj["chapterId"] = chapter_id;//话id
        item_obj["page"] = curr_Page;//第几页
        item_obj["time"] =cookieData//观看时间
        $.cookie("history_Cookie", JSON.stringify([item_obj]),{path:"/",expires: 99999});
    }else{
        var cookie_obj = $.parseJSON($.cookie("history_Cookie"));
        var exist = false;
        for(var i=0;i<cookie_obj.length;i++) {
            var obj = cookie_obj[i];
            if(obj[comic_Id]) {
                obj[comic_Id] = chapter_id;//漫画id
                obj["comicId"] = comic_Id;//漫画id
                obj["chapterId"] = chapter_id;//漫画id
                obj["page"] = curr_Page;//漫画页数
                obj["time"] = cookieData; //观看时间
                exist = true;
                break;
            }
        }
        if(!exist) {
            var item_obj = {};
            item_obj[comic_Id] = chapter_id;
            item_obj["comicId"] = comic_Id;//漫画id
            item_obj["chapterId"] = chapter_id;//漫画id
            item_obj["page"] = curr_Page;
            item_obj["time"] =cookieData;
            cookie_obj.push(item_obj);
        }
        $.cookie("history_Cookie", JSON.stringify(cookie_obj),{path:"/",expires: 99999});
    }

}

setInterval(function (){
    if($.cookie("history_Cookie")!=undefined){
        historyLog($.cookie("history_Cookie"));
    }
    $.cookie("history_Cookie", null,{path:"/"});
},30000);


if($.cookie('display_mode')==null || $.cookie('display_mode')==0){
    getImg_land(picArry);
    $.cookie('display_mode',0,{expires:999999,path:'/'});
    window.onhashchange=function(){
        var his_img = document.location.hash.split("=")[1];
        $(".comic_wraCon").find("img").attr("src",img_prefix+picArry[his_img-1]);
        $("#page_select option").eq(his_img-1).attr("selected","selected");
    };
    $("body").keydown(function(event) {
        if (event.keyCode == 37) {
            prev_img()
        } else if (event.keyCode == 39) {
            next_img()
        }
    });
    $("#mode_1").attr("checked","checked")
}else{
    getImg(picArry);
    $("body").keydown(function(event) {
        if (event.keyCode == 37) {
            if($(".pre a").size()>0){
                if(confirm("要打开上一个章节吗？")==true){
                    location.href = $(".pre a").attr("href");
                }
            }else{
                alert("已经是第一个章节了！")
            }
        } else if (event.keyCode == 39) {
            if($(".next a").size()>0){
                $(".show").show();
                $(".red_box").show();
            }else{
                openBoxOne();
            }
        }
    });
    $("#mode_2").attr("checked","checked")
}

if($.cookie('pic_style')==null || $.cookie('pic_style')==0){
    $.cookie('pic_style',0,{expires:999999,path:'/'});
    $("#sizeF").attr("checked","checked")
}else{
    $("#sizeT").attr("checked","checked");
    setWidth();
}

$(".comic_wraCon").width($(window).width());

window.onresize=function(){
    $(".comic_wraCon").width($(window).width())
};

function reset(){
    var size_c = $("input[name=size]:checked").val();
    var mode_c = $("input[name=mode]:checked").val();
    $.cookie('display_mode',mode_c,{expires:999999,path:'/'});
    $.cookie('pic_style',size_c,{expires:999999,path:'/'});
    location.reload();
}

/*设置图片自适应宽度*/
function setWidth(){
    $(".comic_wraCon img").load(function() {
        var w = $(window).width();//容器宽度
        $(".comic_wraCon img").each(function(){
            var img_w = $(this).width();//图片宽度
            var img_h = $(this).height();//图片高度
            if(img_w>w){//如果图片宽度超出容器宽度--要撑破了
                var height = (w*img_h)/img_w; //高度等比缩放
                $(this).css({"width":w-50,"height":height});//设置缩放后的宽度和高度
            }
        })
    });
}


/*function doHit(){
    cache_id=("undefined"==typeof sns_sys_id)?g_comic_id:sns_sys_id;
    if(!$.cookie('doHit') || $.cookie('doHit')!= cache_id){
        $.cookie('doHit',cache_id,{expires:7,path:'/'});
        var str = "<script src=\"http://s.acg.dmzj.com/comicsum/hit.php?i="+g_comic_id+"&c="+g_comic_code+"\"></script>";
        $('body').append(str);
    }
}*/


function doHit(){
    var str = "<script src=\"//sacg.dmzj.com/comicsum/comicshot.php?i="+g_comic_id+"&cid="+chapter_id+"&signature="+md5("/comicsum/comicshot.php?i="+g_comic_id+"&cid="+chapter_id)+"\"></script>";
    $('body').append(str);
}
doHit();

if($(".btm_chapter_btn").size()==1){
    $(".btmBtnBox").css("width","256px")
}




function md5(string){
    function md5_RotateLeft(lValue, iShiftBits) {
        return (lValue<<iShiftBits) | (lValue>>>(32-iShiftBits));
    }
    function md5_AddUnsigned(lX,lY){
        var lX4,lY4,lX8,lY8,lResult;
        lX8 = (lX & 0x80000000);
        lY8 = (lY & 0x80000000);
        lX4 = (lX & 0x40000000);
        lY4 = (lY & 0x40000000);
        lResult = (lX & 0x3FFFFFFF)+(lY & 0x3FFFFFFF);
        if (lX4 & lY4) {
            return (lResult ^ 0x80000000 ^ lX8 ^ lY8);
        }
        if (lX4 | lY4) {
            if (lResult & 0x40000000) {
                return (lResult ^ 0xC0000000 ^ lX8 ^ lY8);
            } else {
                return (lResult ^ 0x40000000 ^ lX8 ^ lY8);
            }
        } else {
            return (lResult ^ lX8 ^ lY8);
        }
    }
    function md5_F(x,y,z){
        return (x & y) | ((~x) & z);
    }
    function md5_G(x,y,z){
        return (x & z) | (y & (~z));
    }
    function md5_H(x,y,z){
        return (x ^ y ^ z);
    }
    function md5_I(x,y,z){
        return (y ^ (x | (~z)));
    }
    function md5_FF(a,b,c,d,x,s,ac){
        a = md5_AddUnsigned(a, md5_AddUnsigned(md5_AddUnsigned(md5_F(b, c, d), x), ac));
        return md5_AddUnsigned(md5_RotateLeft(a, s), b);
    };
    function md5_GG(a,b,c,d,x,s,ac){
        a = md5_AddUnsigned(a, md5_AddUnsigned(md5_AddUnsigned(md5_G(b, c, d), x), ac));
        return md5_AddUnsigned(md5_RotateLeft(a, s), b);
    };
    function md5_HH(a,b,c,d,x,s,ac){
        a = md5_AddUnsigned(a, md5_AddUnsigned(md5_AddUnsigned(md5_H(b, c, d), x), ac));
        return md5_AddUnsigned(md5_RotateLeft(a, s), b);
    };
    function md5_II(a,b,c,d,x,s,ac){
        a = md5_AddUnsigned(a, md5_AddUnsigned(md5_AddUnsigned(md5_I(b, c, d), x), ac));
        return md5_AddUnsigned(md5_RotateLeft(a, s), b);
    };
    function md5_ConvertToWordArray(string) {
        var lWordCount;
        var lMessageLength = string.length;
        var lNumberOfWords_temp1=lMessageLength + 8;
        var lNumberOfWords_temp2=(lNumberOfWords_temp1-(lNumberOfWords_temp1 % 64))/64;
        var lNumberOfWords = (lNumberOfWords_temp2+1)*16;
        var lWordArray=Array(lNumberOfWords-1);
        var lBytePosition = 0;
        var lByteCount = 0;
        while ( lByteCount < lMessageLength ) {
            lWordCount = (lByteCount-(lByteCount % 4))/4;
            lBytePosition = (lByteCount % 4)*8;
            lWordArray[lWordCount] = (lWordArray[lWordCount] | (string.charCodeAt(lByteCount)<<lBytePosition));
            lByteCount++;
        }
        lWordCount = (lByteCount-(lByteCount % 4))/4;
        lBytePosition = (lByteCount % 4)*8;
        lWordArray[lWordCount] = lWordArray[lWordCount] | (0x80<<lBytePosition);
        lWordArray[lNumberOfWords-2] = lMessageLength<<3;
        lWordArray[lNumberOfWords-1] = lMessageLength>>>29;
        return lWordArray;
    };
    function md5_WordToHex(lValue){
        var WordToHexValue="",WordToHexValue_temp="",lByte,lCount;
        for(lCount = 0;lCount<=3;lCount++){
            lByte = (lValue>>>(lCount*8)) & 255;
            WordToHexValue_temp = "0" + lByte.toString(16);
            WordToHexValue = WordToHexValue + WordToHexValue_temp.substr(WordToHexValue_temp.length-2,2);
        }
        return WordToHexValue;
    };
    function md5_Utf8Encode(string){
        string = string.replace(/\r\n/g,"\n");
        var utftext = "";
        for (var n = 0; n < string.length; n++) {
            var c = string.charCodeAt(n);
            if (c < 128) {
                utftext += String.fromCharCode(c);
            }else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            } else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
        }
        return utftext;
    };
    var x=Array();
    var k,AA,BB,CC,DD,a,b,c,d;
    var S11=7, S12=12, S13=17, S14=22;
    var S21=5, S22=9 , S23=14, S24=20;
    var S31=4, S32=11, S33=16, S34=23;
    var S41=6, S42=10, S43=15, S44=21;
    string = md5_Utf8Encode(string);
    x = md5_ConvertToWordArray(string);
    a = 0x67452301; b = 0xEFCDAB89; c = 0x98BADCFE; d = 0x10325476;
    for (k=0;k<x.length;k+=16) {
        AA=a; BB=b; CC=c; DD=d;
        a=md5_FF(a,b,c,d,x[k+0], S11,0xD76AA478);
        d=md5_FF(d,a,b,c,x[k+1], S12,0xE8C7B756);
        c=md5_FF(c,d,a,b,x[k+2], S13,0x242070DB);
        b=md5_FF(b,c,d,a,x[k+3], S14,0xC1BDCEEE);
        a=md5_FF(a,b,c,d,x[k+4], S11,0xF57C0FAF);
        d=md5_FF(d,a,b,c,x[k+5], S12,0x4787C62A);
        c=md5_FF(c,d,a,b,x[k+6], S13,0xA8304613);
        b=md5_FF(b,c,d,a,x[k+7], S14,0xFD469501);
        a=md5_FF(a,b,c,d,x[k+8], S11,0x698098D8);
        d=md5_FF(d,a,b,c,x[k+9], S12,0x8B44F7AF);
        c=md5_FF(c,d,a,b,x[k+10],S13,0xFFFF5BB1);
        b=md5_FF(b,c,d,a,x[k+11],S14,0x895CD7BE);
        a=md5_FF(a,b,c,d,x[k+12],S11,0x6B901122);
        d=md5_FF(d,a,b,c,x[k+13],S12,0xFD987193);
        c=md5_FF(c,d,a,b,x[k+14],S13,0xA679438E);
        b=md5_FF(b,c,d,a,x[k+15],S14,0x49B40821);
        a=md5_GG(a,b,c,d,x[k+1], S21,0xF61E2562);
        d=md5_GG(d,a,b,c,x[k+6], S22,0xC040B340);
        c=md5_GG(c,d,a,b,x[k+11],S23,0x265E5A51);
        b=md5_GG(b,c,d,a,x[k+0], S24,0xE9B6C7AA);
        a=md5_GG(a,b,c,d,x[k+5], S21,0xD62F105D);
        d=md5_GG(d,a,b,c,x[k+10],S22,0x2441453);
        c=md5_GG(c,d,a,b,x[k+15],S23,0xD8A1E681);
        b=md5_GG(b,c,d,a,x[k+4], S24,0xE7D3FBC8);
        a=md5_GG(a,b,c,d,x[k+9], S21,0x21E1CDE6);
        d=md5_GG(d,a,b,c,x[k+14],S22,0xC33707D6);
        c=md5_GG(c,d,a,b,x[k+3], S23,0xF4D50D87);
        b=md5_GG(b,c,d,a,x[k+8], S24,0x455A14ED);
        a=md5_GG(a,b,c,d,x[k+13],S21,0xA9E3E905);
        d=md5_GG(d,a,b,c,x[k+2], S22,0xFCEFA3F8);
        c=md5_GG(c,d,a,b,x[k+7], S23,0x676F02D9);
        b=md5_GG(b,c,d,a,x[k+12],S24,0x8D2A4C8A);
        a=md5_HH(a,b,c,d,x[k+5], S31,0xFFFA3942);
        d=md5_HH(d,a,b,c,x[k+8], S32,0x8771F681);
        c=md5_HH(c,d,a,b,x[k+11],S33,0x6D9D6122);
        b=md5_HH(b,c,d,a,x[k+14],S34,0xFDE5380C);
        a=md5_HH(a,b,c,d,x[k+1], S31,0xA4BEEA44);
        d=md5_HH(d,a,b,c,x[k+4], S32,0x4BDECFA9);
        c=md5_HH(c,d,a,b,x[k+7], S33,0xF6BB4B60);
        b=md5_HH(b,c,d,a,x[k+10],S34,0xBEBFBC70);
        a=md5_HH(a,b,c,d,x[k+13],S31,0x289B7EC6);
        d=md5_HH(d,a,b,c,x[k+0], S32,0xEAA127FA);
        c=md5_HH(c,d,a,b,x[k+3], S33,0xD4EF3085);
        b=md5_HH(b,c,d,a,x[k+6], S34,0x4881D05);
        a=md5_HH(a,b,c,d,x[k+9], S31,0xD9D4D039);
        d=md5_HH(d,a,b,c,x[k+12],S32,0xE6DB99E5);
        c=md5_HH(c,d,a,b,x[k+15],S33,0x1FA27CF8);
        b=md5_HH(b,c,d,a,x[k+2], S34,0xC4AC5665);
        a=md5_II(a,b,c,d,x[k+0], S41,0xF4292244);
        d=md5_II(d,a,b,c,x[k+7], S42,0x432AFF97);
        c=md5_II(c,d,a,b,x[k+14],S43,0xAB9423A7);
        b=md5_II(b,c,d,a,x[k+5], S44,0xFC93A039);
        a=md5_II(a,b,c,d,x[k+12],S41,0x655B59C3);
        d=md5_II(d,a,b,c,x[k+3], S42,0x8F0CCC92);
        c=md5_II(c,d,a,b,x[k+10],S43,0xFFEFF47D);
        b=md5_II(b,c,d,a,x[k+1], S44,0x85845DD1);
        a=md5_II(a,b,c,d,x[k+8], S41,0x6FA87E4F);
        d=md5_II(d,a,b,c,x[k+15],S42,0xFE2CE6E0);
        c=md5_II(c,d,a,b,x[k+6], S43,0xA3014314);
        b=md5_II(b,c,d,a,x[k+13],S44,0x4E0811A1);
        a=md5_II(a,b,c,d,x[k+4], S41,0xF7537E82);
        d=md5_II(d,a,b,c,x[k+11],S42,0xBD3AF235);
        c=md5_II(c,d,a,b,x[k+2], S43,0x2AD7D2BB);
        b=md5_II(b,c,d,a,x[k+9], S44,0xEB86D391);
        a=md5_AddUnsigned(a,AA);
        b=md5_AddUnsigned(b,BB);
        c=md5_AddUnsigned(c,CC);
        d=md5_AddUnsigned(d,DD);
    }
    return (md5_WordToHex(a)+md5_WordToHex(b)+md5_WordToHex(c)+md5_WordToHex(d)).toLowerCase();
}

```
<font color=#999AAA >哎哟，你看这不就来了吗？这里面有一个getImg()方法，一看给的注释是竖屏显示图片。
显示图片说明什么？说明肯定传入了图片的数据啊，由此可见传入的参数data就是代表的图片数据
我们直接在当前js文件里面搜索getImg，果不其然，在278行找到了一个getImg(picArry)。
由此可见，picArry就是我们要找的
我们在文件开头的地方就能看到picArry的身影

```javascript
pages = pages.replace(/\n/g,"");
pages = pages.replace(/\r/g,"|");
var info = eval("(" + pages + ")");
var picArry = info['page_url'].split("|");
```
所以我们最终的目标锁定在了pages上。
那这个pages哪来的了？
这还不简单，我们直接去top文件夹下搜索该js文件名称，看哪个html调用过不就知道了吗？
最终在当前网页中找到了pages
![在这里插入图片描述](https://img-blog.csdnimg.cn/4d05e6b744d84c44b21639c57d98f685.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA56ia5bCP55m9,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
eval(...)执行完后就会返回一个pages，里面就存放这所有的图片链接。



# 二、代码实现

```python
import os
import requests
from bs4 import BeautifulSoup


# 图片防盗链，想要请求的话需要带上Referer
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
#     'Referer': 'https://www.dmzj.com/',
#     'Host': 'images.dmzj.com'
# }
# res = requests.get("https://images.dmzj.com/img/chapterpic/28739/110239/15560700290294.jpg", headers=headers)
# print(res.text)

# 写入以及执行的js文件名
JS_FILE_NAME = "dmzj.js"


# 获取指定网页内的js代码
def getJSCode(htmlUrl):
    res = requests.get(htmlUrl)
    bs = BeautifulSoup(res.text, "html.parser")
    content = str(bs.find("script")).split('<script type="text/javascript">')[1].split("</script>")[0]
    return content


# 将爬取到的js代码写入到指定文件中
def writeJS(code):
    code = code + """
        function getData(code) {
            pages = pages.replace(/\\n/g,"");
            pages = pages.replace(/\\r/g,"|");
            var info = eval("(" + pages + ")");
            var picArry = info['page_url'].split("|");
            var pic = [];
            for (let i = 0; i < picArry.length; i ++) {
                pic[i] = "https://images.dmzj.com/" + picArry[i];
            }
            return pic;
        }
        console.log(getData());
    """
    with open(JS_FILE_NAME, "w") as f:
        f.write(code)


# 调用node.js 执行js文件 并输出结果
def execJSFile(htmlUrl):
    writeJS(getJSCode(htmlUrl))
    result = os.popen('node ' + JS_FILE_NAME)
    print(result.read())


if __name__ == '__main__':
    execJSFile("https://www.dmzj.com/view/jinshangxiang/83369.html")
```

<font color=#999AAA >我这说下怎么写的嗷
我们先获取到那段js代码，然后进行一个处理，最终写入到一个js文件中去。然后我们通过python调用node.js执行该js文件最终返回结果。所以想测试的话需要安装node.js。dmzj的图片都有防盗链，所以需要在请求头里加上Referer。
<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">
