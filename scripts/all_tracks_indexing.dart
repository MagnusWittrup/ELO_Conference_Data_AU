import 'dart:convert';
import 'dart:io';

main(List<String> args) {
  final foldersToIndex = _getAllValidFolderURIs();

  for (final fileToIndex in foldersToIndex) {
    final Map<String, List<String>> speakerMap = {};
    final fileText = _getCleanStringWithoutVttInfo(fileToIndex);
    final fileTextLines = fileText.split('\n');
    for (final fileTextLine in fileTextLines) {
      final speakerAndText = _getSpeakerTextPairingFromTextLine(fileTextLine);
      if (speakerAndText == null) {
        continue;
      }
      if (speakerMap.containsKey(speakerAndText.speaker)) {
        speakerMap[speakerAndText.speaker]?.add(speakerAndText.text);
      } else {
        speakerMap[speakerAndText.speaker] = [speakerAndText.text];
      }
    }

    final _pathSegmentsToFile = fileToIndex.pathSegments.sublist(0);
    _pathSegmentsToFile.removeLast();
    final _pathToFile = _pathSegmentsToFile.join('/');
    print(_pathToFile);

    Directory('./output/' + _pathToFile).createSync(recursive: true);
    print('WRITING TO : ' + '/' + fileToIndex.path);
    writeFile('/' + fileToIndex.path, jsonEncode(speakerMap));
    writeFile('/' + fileToIndex.pathSegments.join('_'), jsonEncode(speakerMap));
  }
}

List<Uri> _getAllValidFolderURIs() {
  final List<Uri> output = [];
  final dataDirectory = Directory('./data');

  final dataSubDirectories = dataDirectory.listSync();
  for (final dataSubDirectory in dataSubDirectories) {
    if (dataSubDirectory is! Directory || dataSubDirectory.listSync().length < 1) {
      continue;
    }
    // print("\n ------------- ${dataSubDirectory} ------------- ");

    final dataDateSubDirectories = dataSubDirectory.listSync();
    for (final dataDateSubDirectory in dataDateSubDirectories) {
      if (dataDateSubDirectory is! Directory || dataDateSubDirectory.listSync().length < 1) {
        continue;
      }

      // print("\n ------ ${dataDateSubDirectory} ------ ");

      final dataDateTrackSubDirectories = dataDateSubDirectory.listSync();
      for (final dataDateTrackSubDirectory in dataDateTrackSubDirectories) {
        if (dataDateTrackSubDirectory is! Directory || dataDateTrackSubDirectory.listSync().length < 1) {
          continue;
        }

        // print("\n -- ${dataDateTrackSubDirectory} -- ");
        final dataDateTrackTitleSubDirectories = dataDateTrackSubDirectory.listSync();
        for (final dataDateTrackTitleSubDirectory in dataDateTrackTitleSubDirectories) {
          if (dataDateTrackTitleSubDirectory.toString().contains('.transcript.')) {
            output.add(dataDateTrackTitleSubDirectory.uri);
            // print(dataDateTrackTitleSubDirectory);
          }
        }
      }
    }
  }
  return output;
}

String _getCleanStringWithoutVttInfo(Uri uri) {
  final fileFromUri = File.fromUri(uri);
  final vttTimestampAndNumberRegex = RegExp(r'^([0-9]+\n|)([0-9:,->\s]+)', multiLine: true);
  final fileText = fileFromUri.readAsStringSync();
  return fileText.replaceAll(vttTimestampAndNumberRegex, '\n').replaceAll('WEBVTT', '');
}

class SpeakerText {
  final String speaker;
  final String text;

  const SpeakerText({
    required this.speaker,
    required this.text,
  });

  @override
  String toString() => '''
SpeakerText(
  speaker: $speaker, 
  text: $text,
)
  ''';
}

SpeakerText? _getSpeakerTextPairingFromTextLine(String textLine) {
  final splitSpeakerAndText = textLine.split(':');
  if (splitSpeakerAndText.isEmpty) {
    return null;
  }
  String speaker;
  String text;
  if (splitSpeakerAndText.length == 1) {
    speaker = 'unknown';
    text = splitSpeakerAndText[0];
  } else {
    speaker = splitSpeakerAndText[0];
    text = splitSpeakerAndText[1];
  }
  if (text.isEmpty) {
    return null;
  }
  return SpeakerText(speaker: speaker, text: text);
}

void writeFile(String fileName, String data, {String folder = "./output", String fileType = ".json"}) {
  final outputPath = folder + fileName + fileType;
  final outputFile = File(outputPath);
  outputFile.existsSync() ? outputFile.writeAsStringSync(data) : outputFile.create().then((file) => file.writeAsStringSync(data));
}
