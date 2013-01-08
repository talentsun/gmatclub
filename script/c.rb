require 'net/http'
require 'sqlite3'

$url_prefix = "http://www.kaogmat.com/"
$types = ['sc', 'cr', 'rc', 'ps', 'ds', 'ir', 'awa']
$db_name = "result.sqlite"

def get_url(type, page) 
  $url_prefix + type + '?p=' + page.to_s
end

def process_type_page(type, page)
  uri = URI(get_url(type, page))
  ret = Net::HTTP.get(uri)
  puts ret

  SQLite3::Database.new($db_name)
end

def process_type(type) 
  (1..1000).each do |page|
    process_type_page(type, page)
    break
  end
end

def start_page
  $types.each do |type|
    process_type(type)
  end
end


start_page
