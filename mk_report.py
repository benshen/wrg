# Function: To generate excel document
# Author: xiaoben
# Email: xiaoben@outlook.com
# Date:  2014-5-16

import sys
import os
import datetime
from xlwt import Workbook, XFStyle, Borders, Pattern, Font, Alignment


def from_this_dir(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def generate_report(root, filename, attend_staff, absent_staff, meeting_direct, record_staff, reports, issues):
    book = Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('Fota Security Knox Week Report')
    line_counter = 0

    today = datetime.date.today().strftime('%Y/%m/%d')
    # header
    head_str = [
        'Meeting Name', 'SW 3 Group Part 5 Fota/ Security/Knox/Encription TG WeekReport',
        '', '',
        'Meeting Date', today,
        'Meeting Address', '8F Meeting Room',
        '', '',
        'Attend Staff', attend_staff,
        'Absent Staff', absent_staff,
        '', '',
        'Meeting Direct', meeting_direct,
        'Record Staff', record_staff,
    ]

    for i in range(len(head_str) / 2):
        sheet1.row(i).write(0, head_str[2 * i])
        sheet1.row(i).write(1, head_str[2 * i + 1])
    line_counter = len(head_str) / 2 + 1

    # font bold
    font = Font()
    font.bold = True
    # pattern yellow
    pattern_yellow = Pattern()
    pattern_yellow.pattern = Pattern.SOLID_PATTERN
    pattern_yellow.pattern_fore_colour = 0x0D  # yellow
    # pattern gray
    pattern_gray = Pattern()
    pattern_gray.pattern = Pattern.SOLID_PATTERN
    pattern_gray.pattern_fore_colour = 0x17  # gray
    # borders thin
    borders = Borders()
    borders.left = Borders.THIN
    borders.right = Borders.THIN
    borders.top = Borders.THIN
    borders.bottom = Borders.THIN
    # alignment horizontal center
    alig_hc = Alignment()
    # alig.horizontal = Alignment.HORZ_CENTER #no effect, why? fuck!!!
    alig_hc.horz = Alignment.HORZ_CENTER

    # title style
    style_title = XFStyle()
    style_title.font = font
    style_title.pattern = pattern_yellow
    style_title.alignment = alig_hc
    sheet1.write_merge(
        line_counter, line_counter, 0, 3, 'summary', style_title)

    line_counter += 1

    # table header style
    sytle_tb_header = XFStyle()
    sytle_tb_header.font = font
    sytle_tb_header.pattern = pattern_gray
    sytle_tb_header.borders = borders
    sytle_tb_header.alignment = alig_hc

    sheet1.row(line_counter).write(0, 'Member', sytle_tb_header)
    sheet1.row(line_counter).write(1, 'Week Jobs', sytle_tb_header)
    sheet1.row(line_counter).write(2, 'Risk', sytle_tb_header)
    sheet1.row(line_counter).write(3, 'Next Week Plan', sytle_tb_header)
    line_counter += 1

    # content

    # for i in range(line_counter,11+line_counter):
    i = line_counter
    for report in reports:
        # alignment
        alig = Alignment()
        alig.horz = Alignment.HORZ_CENTER
        alig.vert = Alignment.VERT_CENTER
        alig.wrap = 1

        # alignment2
        alig2 = Alignment()
        alig2.vert = Alignment.VERT_CENTER
        alig2.wrap = 1

        # borders
        borders = Borders()
        borders.left = Borders.THIN
        borders.right = Borders.THIN
        borders.top = Borders.THIN
        borders.bottom = Borders.THIN
        # colors
        pattern = Pattern()
        pattern.pattern = Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 0x2F

        style_content = XFStyle()
        style_content.alignment = alig
        style_content.borders = borders

        style_content2 = XFStyle()
        style_content2.alignment = alig2
        style_content2.borders = borders
        style_content2.pattern = pattern

        style_content3 = XFStyle()
        style_content3.alignment = alig2
        style_content3.borders = borders

        sheet1.row(i).write(0, report.who, style_content)
        sheet1.row(i).write(1, report.job, style_content2)
        sheet1.row(i).write(2, report.risk, style_content2)
        sheet1.row(i).write(3, report.plan, style_content3)

        sheet1.row(i).height_mismatch = True
        sheet1.row(i).height = 1500
        i += 1

    line_counter += len(reports)
    line_counter += 1

    sheet1.write_merge(
        line_counter, line_counter, 0, 3, 'Main Issues List', style_title)
    line_counter += 1

    sheet1.row(line_counter).write(0, 'Items', sytle_tb_header)
    sheet1.write_merge(
        line_counter, line_counter, 1, 2, 'Deatail', sytle_tb_header)
    sheet1.row(line_counter).write(3, 'Status', sytle_tb_header)
    line_counter += 1

    sheet1.col(0).width = 256 * 16
    sheet1.col(1).width = 256 * 50
    sheet1.col(2).width = 256 * 31
    sheet1.col(3).width = 256 * 46

    book.save(root + '/' + filename)
