import libarchive.public
import libarchive.constants

for entry in libarchive.public.create_file(
    'test.7z',
    libarchive.constants.ARCHIVE_FORMAT_7ZIP,
    ['data/eva_time_data_1.in', 'data/eva_time_data_2.in', 'data/eva_time_data_3.in']):
  print entry
