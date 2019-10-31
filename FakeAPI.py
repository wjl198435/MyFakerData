from faker import Faker
f = Faker(locale='zh_CN')
f.city_suffix() #市，县

f.country() #国家

f.country_code() #国家编码

f.district() #区

# f.geo_coordinate() #地理坐标

f.latitude() #地理坐标(纬度)

f.longitude() #地理坐标(经度)

f.lexify() #替换所有问号（“？”）带有随机字母的事件。

f.numerify() #三位随机数字

f.postcode() #邮编

f.province() #省份

f.street_address() #街道地址

f.street_name() #街道名

f.street_suffix() #街、路

f.random_digit() #0~9随机数

f.random_digit_not_null() #1~9的随机数

f.random_element() #随机字母

f.random_int() #随机数字，默认0~9999，可以通过设置min,max来设置

f.random_letter() #随机字母

f.random_number() #随机数字，参数digits设置生成的数字位数

f.color_name() #随机颜色名

f.hex_color() #随机HEX颜色

f.rgb_color() #随机RGB颜色

f.safe_color_name() #随机安全色名

f.safe_hex_color() #随机安全HEX颜色

f.bs() #随机公司服务名

f.company() #随机公司名（长）

f.company_prefix() #随机公司名（短）

f.company_suffix() #公司性质

f.credit_card_expire() #随机信用卡到期日

f.credit_card_full() #生成完整信用卡信息

f.credit_card_number() #信用卡号

f.credit_card_provider() #信用卡类型

f.credit_card_security_code() #信用卡安全码

f.currency_code() #货币编码

f.am_pm() #AM/PM

f.century() #随机世纪

f.date() #随机日期

f.date_between() #随机生成指定范围内日期，参数 #start_date，end_date取值 #具体日期或者today,-30d,-30y类似

f.date_between_dates() #随机生成指定范围内日期，用法同上

f.date_object() #随机生产从1970-1-1到指定日期的随机日期。

f.date_this_month() #

f.date_this_year() #

f.date_time() #随机生成指定时间（1970年1月1日至今）

f.date_time_ad() #生成公元1年到现在的随机时间

f.date_time_between() #用法同dates

f.future_date() #未来日期

f.future_datetime() #未来时间

f.month() #随机月份

f.month_name() #随机月份（英文）

f.past_date() #随机生成已经过去的日期

f.past_datetime() #随机生成已经过去的时间

f.time() #随机24小时时间

# f.timedelta() #随机获取时间差

f.time_object() #随机24小时时间，time对象

f.time_series() #随机TimeSeries对象

f.timezone() #随机时区

f.unix_time() #随机Unix时间

f.year() #随机年份

f.file_extension() #随机文件扩展名

f.file_name() #随机文件名（包含扩展名，不包含路径）

f.file_path() #随机文件路径（包含文件名，扩展名）

f.mime_type() #随机mime Type

f.ascii_company_email() #随机ASCII公司邮箱名

f.ascii_email() #随机ASCII邮箱

f.ascii_free_email() #

f.ascii_safe_email() #

f.company_email() #

f.domain_name() #生成域名

f.domain_word() #域词(即，不包含后缀)

f.email() #

f.free_email() #

f.free_email_domain() #

f.safe_email() #安全邮箱

f.image_url() #随机URL地址

f.ipv4() #随机IP4地址

f.ipv6() #随机IP6地址

f.mac_address() #随机MAC地址

f.tld() #网址域名后缀(.com,.net.cn,等等，不包括.)

f.uri() #随机URI地址

f.uri_extension() #网址文件后缀

f.uri_page() #网址文件（不包含后缀）

f.uri_path() #网址文件路径（不包含文件名）

f.url() #随机URL地址

f.user_name() #随机用户名

f.isbn10() #随机ISBN（10位）

f.isbn13() #随机ISBN（13位）

f.job() #随机职位

f.paragraph() #随机生成一个段落

f.paragraphs() #随机生成多个段落，通过参数nb来控制段落数，返回数组

f.sentence() #随机生成一句话

f.sentences() #随机生成多句话，与段落类似

f.text() #随机生成一篇文章（不要幻想着人工智能了，至今没完全看懂一句话是什么意思）

f.word() #随机生成词语

f.words() #随机生成多个词语，用法与段落，句子，类似

f.binary() #随机生成二进制编码

f.boolean() #True/False

f.language_code() #随机生成两位语言编码

f.locale() #随机生成语言/国际 信息

f.md5() #随机生成MD5

f.null_boolean() #NULL/True/False

f.password() #随机生成密码,可选参数 #length #密码长度；special_chars #是否能使用特殊字符；digits #是否包含数字；upper_case #是否包含大写字母；lower_case #是否包含小写字母

f.sha1() #随机SHA1

f.sha256() #随机SHA256

f.uuid4() #随机UUID

f.first_name() #

f.first_name_female() #女性名

f.first_name_male() #男性名

f.first_romanized_name() #罗马名

f.last_name() #

f.last_name_female() #女姓

f.last_name_male() #男姓

f.last_romanized_name() #

f.name() #随机生成全名

f.name_female() #男性全名

f.name_male() #女性全名

f.romanized_name() #罗马名

f.msisdn() #移动台国际用户识别码，即移动用户的ISDN号码

f.phone_number() #随机生成手机号

f.phonenumber_prefix() #随机生成手机号段

print(f.profile()) #随机生成档案信息

f.simple_profile() #随机生成简单档案信息