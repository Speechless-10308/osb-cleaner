# OSB Cleaner
A simple and small tool to detect unused files in osu! beatmap (especially in storyboard) and provide the option to delete them.

## Usage
### The fastest way for those who have python:
1. Clone the repo:
```sh
git clone git@github.com:Speechless-10308/osb-cleaner.git
```
2. Enter the target dir.
3. Type the following command:
```sh
python detector.py --mapset-dir <dir to mapset>
```

## Example

```sh
python detector.py --mapset-dir "E:/osu/Songs/123456 Example Mapset"
```

### If you do not have python, ~~just download one~~
1. Download the release stuff.
2. Enter the target dir.
3. Type the following command:
```sh
detector.exe --mapset-dir <dir to mapset>
```

## Warning!
- It is recommended to back up the beatmap directory before deleting files.
- The detection results of this tool may not be completely accurate (I am stupid). It is recommended to check it in conjunction with Mapset Verifier.

## Contribution
Feel free to add new feature for this project. Raise them in issue or pull a request.

## License
This project uses MIT license.
