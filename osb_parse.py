import os


class OsuStoryboard():
    def __init__(self, mapset_path: str, osb_filepath: str):
        self.osb_path = osb_filepath
        self.mapset_path = mapset_path
        self.osu_files = self.__osu_files()
        self.used_sprite = set()
        self.__parse_osb()
        self.__update_used_file()
    
    def __osu_files(self):
        osu_files = set()
        for root, dirs, files in os.walk(self.mapset_path):
            for file in files:
                if file.endswith('.osu'):
                    osu_files.add(os.path.relpath(os.path.join(root, file), self.mapset_path).replace('\\', '/'))
        return osu_files
    
    def __update_used_file(self):
        self.used_file = set()
        for osu_file in self.osu_files:
            with open(os.path.join(self.mapset_path, osu_file), 'r', encoding='utf-8') as f:
                lines = f.read().split('\n')
                try:
                    index_events = lines.index("[Events]")
                    index_timing_points = lines.index("[TimingPoints]")
                except ValueError:
                    print(f'Unsupported file format: {osu_file}')
                    continue
                # parse events
                detect_bg = False

                for line in lines[:index_events]:
                    keyword, *values = line.split(':')
                    if keyword == "AudioFilename":
                        audio_path = values[0].strip()
                        if audio_path not in self.used_file:
                            self.used_file.add(audio_path)

                for line in lines[index_events + 1:index_timing_points]:
                    if line.startswith('//Background and Video events'):
                        detect_bg = True
                        continue

                    if detect_bg:
                        bg_path = line.split(',')[2].replace('\\', '/').strip('"')
                        if bg_path not in self.used_sprite:
                            self.used_sprite.add(bg_path)
                        detect_bg = False
                        
                    if 'Sprite,' in line:
                        sprite_path = line.split(',')[3].replace('\\', '/').strip('"')
                        if sprite_path not in self.used_sprite:
                            self.used_sprite.add(sprite_path)


        self.used_file.update(self.used_sprite)
        self.used_file.update(self.osu_files)
        
    def __parse_osb(self):
        with open(self.osb_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'Sprite,' in line:
                    sprite_path = line.split(',')[3].replace('\\', '/').strip('"')
                    if sprite_path not in self.used_sprite:
                        self.used_sprite.add(sprite_path)

                if 'Animation,' in line:
                    animation_path = line.split(',')[3].replace('\\', '/').strip('"')
                    # also need to check the animation frames
                    frame_count = line.split(',')[6]
                    for i in range(int(frame_count)):
                        # change original path, add the postfix.
                        # example: 'path/s.png' to 'path/s0.png'
                        # example2: 'path/s.jpeg' to 'path/s1.jpeg'
                        base, ext = os.path.splitext(animation_path)
                        new_path = f"{base}{i}{ext}"
                        if new_path not in self.used_sprite:
                            self.used_sprite.add(new_path)

        for osu_file in self.osu_files:
            with open(os.path.join(self.mapset_path, osu_file), 'r', encoding='utf-8') as f:
                for line in f:
                    if 'Sprite,' in line:
                        sprite_path = line.split(',')[3].replace('\\', '/').strip('"')
                        if sprite_path not in self.used_sprite:
                            self.used_sprite.add(sprite_path)
                    
                    if 'Animation,' in line:
                        animation_path = line.split(',')[3].replace('\\', '/').strip('"')
                        # also need to check the animation frames
                        frame_count = line.split(',')[6]
                        for i in range(int(frame_count)):
                            # change original path, add the postfix.
                            # example: 'path/s.png' to 'path/s0.png'
                            # example2: 'path/s.jpeg' to 'path/s1.jpeg'
                            base, ext = os.path.splitext(animation_path)
                            new_path = f"{base}{i}{ext}"
                            if new_path not in self.used_sprite:
                                self.used_sprite.add(new_path)


    def detect_unused_file(self, mapset_dir: str):
        unused_files = []
        for root, dirs, files in os.walk(mapset_dir):
            for file in files:
                file = os.path.relpath(os.path.join(root, file), mapset_dir).replace('\\', '/')


                if file.endswith('.mp3') or file.endswith('.wav') or file.endswith('.ogg') or file.endswith('.osb'):
                    continue
                if file not in self.used_file:
                    unused_files.append(file)
        return unused_files
        

