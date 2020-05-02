require_relative 'runall'
require 'watir'
require 'csv'
require 'selenium-webdriver'
require 'rufus-scheduler'

scheduler = Rufus::Scheduler.new

options = Selenium::WebDriver::Chrome::Options.new(args: ['--blink-settings=imagesEnabled=false'])

options.add_extension('./chrome_extension.crx')


browser = Watir::Browser.new :chrome, options: options

browser.goto("https://conso-api.vod-prime.space/set_robot")


#log in
browser.goto("https://www.netflix.com/login")

sleep(5)
browser.text_field(id: "id_userLoginId").set "gbideau@emns.fr"
browser.text_field(id: "id_password").set "torredikiev1928"
browser.button(:xpath => "//*[@id='appMountPoint']/div/div[3]/div/div/div[1]/form/button").click
puts "login ok"

#create profile
sleep(5)
browser.goto("https://www.netflix.com/profiles/manage")
browser.div(class: "addProfileIcon").click
browser.text_field(id: "add-profile-name").set "#{$profile1_username}"
browser.span(:xpath => "/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/span[1]").click
browser.goto("https://www.netflix.com/browse")
browser.span(text: "#{$profile1_username}").click
browser.button(class: "close-button").click
# browser.goto("https://www.netflix.com/DoNotTest")
# browser.label(class:"uiToggleSwitch").click
browser.goto("https://www.netflix.com/browse")
puts "profile ok"
sleep(5)

browser.window.maximize

#scroll to bottom
loop do
    link_number = browser.links.size
    browser.scroll.to :bottom
    sleep(5)
    break if browser.links.size == link_number
end
sleep(5)
browser.scroll.by 0, 300
sleep(2)
browser.scroll.to :top
puts "scroll ok"

thumbs = Array.new
thumbs << "raw_info;section_title;title_id;row;rank"

#billboard
billboard = browser.div(class:"billboard-links").a.href
billboard_id = billboard.match(/(?<=\/)([0-9]*?)(?=\?)/).to_s
thumbs << "#{billboard_id} | billboard;billboard;#{billboard_id};0;0"
print "parsing homepage row: 0"

#rows
row = browser.divs(class: "lolomoRow")
row.each do |n|

    #normal row with pagination
    if n.span(class: "handleNext").exists?
        rowHeader = n.div(class: "row-header-title").text
        loop do
            pagination = n.lis(:xpath => ".//*[@class='pagination-indicator']/li")
            thumbnails = n.divs(class: ["slider-refocus", "title-card"])
            thumbnails.each do |p|
                item = p.div(class: "ptrack-content").a.href
                title_id = item.match(/(?<=\/)([0-9]*?)(?=\?)/)
                position = p.attribute_value("id")
                row_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=-)/)
                rank_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=$)/)
                raw_position = "#{title_id} | #{position}"
                thumbs << "#{raw_position};#{rowHeader};#{title_id};#{row_number};#{rank_number}"
                print "\rparsing homepage row: #{row_number}"
                #row_number.uniq
            end


            #click on right arrows on each row
            n.span(class: "handleNext").click
            sleep(2)
            break if pagination.last.class_name.include?("active")
        end
        #normal row - no pagination
    elsif n.span(class: "rowTitle").exists?
        rowHeader = n.div(class: "row-header-title").text
        thumbnails = n.divs(class: ["slider-refocus", "title-card"])
        thumbnails.each do |p|
            item = p.div(class: "ptrack-content").a.href
            title_id = item.match(/(?<=\/)([0-9]*?)(?=\?)/)
            position = p.attribute_value("id")
            row_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=-)/)
            rank_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=$)/)
            raw_position = "#{title_id} | #{position}"
            thumbs << "#{raw_position};#{rowHeader};#{title_id};#{row_number};#{rank_number}"
            print "\rparsing homepage row: #{row_number}"
        end

        #big row - no pagination
    elsif n.div(class: "bigRow").exists?
        browser.scroll.by 0, 300
        bigRow = n.div(class: "bigRow")
        bigRowtitle_id = n.div(class:"ptrack-content").attribute_value("data-ui-tracking-context").match(/(?<=%22video_id%22:)([0-9]*?)(?=,)/)
        row_num = bigRow.attribute_value("id").match(/(?<=-)([0-9]*?)(?=$)/)
        thumbs << "#{bigRowtitle_id} | BigRow;BigRow;#{bigRowtitle_id};#{row_num};0"
        print "\rparsing homepage row: #{row_num}"
    end
end

thumbs_uniq = thumbs.uniq
thumbs_final = thumbs_uniq.join("\n")

time = Time.now.to_date.to_s

File.write("results_#{time}_#{$profile1_username}_snap1.csv", thumbs_final)

#content1
browser.goto("https://www.netflix.com/watch/#{$profile1_content1}")
puts "\n#{browser.url}"
Watir::Wait.until(timeout: 10800) { browser.div(class: "PromotedVideo").present? || browser.span(class: "ltr-18i00qw").present? }

# #content2
browser.goto("https://www.netflix.com/watch/#{$profile1_content2}")
Watir::Wait.until(timeout: 10800) { browser.div(class: "PromotedVideo").present? || browser.span(class: "ltr-18i00qw").present? }

browser.close

scheduler.at "#{$day2}" do

    browser = Watir::Browser.new :chrome, options: options

    browser.goto("https://www.netflix.com/login")

    browser.text_field(id: "id_userLoginId").set "gbideau@emns.fr"
    browser.text_field(id: "id_password").set "torredikiev1928"
    browser.button(:xpath => "//*[@id='appMountPoint']/div/div[3]/div/div/div[1]/form/button").click
    puts "login ok"

    browser.span(text: "#{$profile1_username}").click

    browser.window.maximize

    # #content3
    browser.goto("https://www.netflix.com/watch/#{$profile1_content3}")
    Watir::Wait.until(timeout: 10800) { browser.div(class: "PromotedVideo").present? || browser.span(class: "ltr-18i00qw").present? }

    # #content4
    browser.goto("https://www.netflix.com/watch/#{$profile1_content4}")
    Watir::Wait.until(timeout: 10800) { browser.div(class: "PromotedVideo").present? || browser.span(class: "ltr-18i00qw").present? }

    #homepage
    browser.goto("https://www.netflix.com/browse")
    sleep(5)

    #scroll to bottom
    loop do
        link_number = browser.links.size
        browser.scroll.to :bottom
        sleep(5)
        break if browser.links.size == link_number
    end
    sleep(5)
    browser.scroll.by 0, 300
    sleep(2)
    browser.scroll.to :top
    puts "scroll ok"

    thumbs2 = Array.new
    thumbs2 << "raw_info;section_title;title_id;row;rank"

    #billboard
    billboard = browser.div(class:"billboard-links").a.href
    billboard_id = billboard.match(/(?<=\/)([0-9]*?)(?=\?)/).to_s
    thumbs2 << "#{billboard_id} | billboard;billboard;#{billboard_id};0;0"
    print "parsing homepage row: 0"

    #rows
    row = browser.divs(class: "lolomoRow")
    row.each do |n|

        #normal row with pagination
        if n.span(class: "handleNext").exists?
            rowHeader = n.div(class: "row-header-title").text
            loop do
                pagination = n.lis(:xpath => ".//*[@class='pagination-indicator']/li")
                thumbnails = n.divs(class: ["slider-refocus", "title-card"])
                thumbnails.each do |p|
                    item = p.div(class: "ptrack-content").a.href
                    title_id = item.match(/(?<=\/)([0-9]*?)(?=\?)/)
                    position = p.attribute_value("id")
                    row_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=-)/)
                    rank_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=$)/)
                    raw_position = "#{title_id} | #{position}"
                    thumbs2 << "#{raw_position};#{rowHeader};#{title_id};#{row_number};#{rank_number}"
                    print "\rparsing homepage row: #{row_number}"
                    #row_number.uniq
                end


                #click on right arrows on each row
                n.span(class: "handleNext").click
                sleep(2)
                break if pagination.last.class_name.include?("active")
            end
            #normal row - no pagination
        elsif n.span(class: "rowTitle").exists?
            rowHeader = n.div(class: "row-header-title").text
            thumbnails = n.divs(class: ["slider-refocus", "title-card"])
            thumbnails.each do |p|
                item = p.div(class: "ptrack-content").a.href
                title_id = item.match(/(?<=\/)([0-9]*?)(?=\?)/)
                position = p.attribute_value("id")
                row_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=-)/)
                rank_number = p.attribute_value("id").match(/(?<=-)([0-9]*?)(?=$)/)
                raw_position = "#{title_id} | #{position}"
                thumbs2 << "#{raw_position};#{rowHeader};#{title_id};#{row_number};#{rank_number}"
                print "\rparsing homepage row: #{row_number}"
            end

            #big row - no pagination
        elsif n.div(class: "bigRow").exists?
            browser.scroll.by 0, 300
            bigRow = n.div(class: "bigRow")
            bigRowtitle_id = n.div(class:"ptrack-content").attribute_value("data-ui-tracking-context").match(/(?<=%22video_id%22:)([0-9]*?)(?=,)/)
            row_num = bigRow.attribute_value("id").match(/(?<=-)([0-9]*?)(?=$)/)
            thumbs2 << "#{bigRowtitle_id} | BigRow;BigRow;#{bigRowtitle_id};#{row_num};0"
            print "\rparsing homepage row: #{row_num}"
        end
    end

    thumbs_uniq = thumbs2.uniq
    thumbs_final = thumbs_uniq.join("\n")

    time = Time.now.to_date.to_s

    File.write("results_#{time}_#{$profile1_username}_snap2.csv", thumbs_final)
end

scheduler.join

browser.close
