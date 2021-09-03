import 'dart:convert';
import 'dart:io';

void main() {
  Directory dir = Directory('./keynote-data');
  List<FileSystemEntity> entries = dir.listSync(recursive: false).toList();
  final regexSplitter = RegExp(r'(\[.*\] )');
  final regexRemoveSpeaker = RegExp(r' - Speaker \d');

//#region
  for (final entry in entries) {
    Map<String, List<String>> map = {};
    final outputFileName = entry.path.replaceAll('./keynote-data', '');

    final file = (entry as File).readAsStringSync();
    final splitSpeaker = file.split(regexSplitter);
    final cleanFullText =
        file.replaceAll(regexSplitter, '').replaceAll(regexRemoveSpeaker, '');
    writeFile(outputFileName, cleanFullText);

    for (final word in splitSpeaker) {
      final unfilteredList = word.split('\n');
      unfilteredList.removeWhere((element) => element == '');
      if (unfilteredList.length < 2) unfilteredList.insert(0, 'unknown');
      final key = unfilteredList.first.replaceAll('- Speaker ', '');
      final val = unfilteredList.last;

      map[key] != null ? (map[key] as List<String>).add(val) : map[key] = [val];
    }
    final json = jsonEncode(map);
    print(json);

    writeFile(outputFileName, json);

    // final outputPath = "./output" + outputFileName + ".json";
    // final outputFile = File(outputPath);
    // outputFile.existsSync()
    //     ? outputFile.writeAsStringSync(json)
    //     : outputFile.create().then((file) => file.writeAsStringSync(json));

    // outputFile.writeAsStringSync(json);
  }
}

void writeFile(String fileName, String data,
    {String folder = "./output", String fileType = ".json"}) {
  final regex = RegExp(r'\.\w[^\. | $]*\S*');
  final outputPath = "./output" + fileName.replaceAll(regex, "") + fileType;
  final outputFile = File(outputPath);
  outputFile.existsSync()
      ? outputFile.writeAsStringSync(data)
      : outputFile.create().then((file) => file.writeAsStringSync(data));
}
