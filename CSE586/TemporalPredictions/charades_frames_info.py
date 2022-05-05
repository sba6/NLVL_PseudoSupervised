import json

def main():
    columns = ['video-name','t-init','t-end','f-init','f-end','video-duration','frame-rate','video-frames','label-idx']
    json_path = 'charades_annotations.json'
    write_path = 'charades_frames_info.json'
    with open(json_path) as json_file:
        json_dict = json.load(json_file)
        frames_dict = {}
        for vid in json_dict:
            frames_dict[vid] = json_dict[vid]['duration_frame']
    with open(write_path, 'w', encoding='utf8') as write_file:
        json.dump(frames_dict, write_file, ensure_ascii=True)

if __name__ == '__main__':
    main()