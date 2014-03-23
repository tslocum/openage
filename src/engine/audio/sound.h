#ifndef _ENGINE_AUDIO_SOUND_H_
#define _ENGINE_AUDIO_SOUND_H_

#include <memory>

#include "category.h"
#include "resource.h"

namespace engine {
namespace audio {

// forward declaration of AudioManager
class AudioManager;

class SoundImpl {
private:
	std::shared_ptr<Resource> resource;

	int32_t volume;
	uint32_t position;

public:
	SoundImpl(std::shared_ptr<Resource> resource, int32_t volume=128);
	~SoundImpl() = default;

	category_t get_category() const;
	int get_id() const;

private:
	/*
	 * Mix this sound and return whether it has finished or not.
	 */
	bool mix_audio(int32_t *stream, int len);

	friend class AudioManager;
};

class Sound {
private:
	AudioManager *audio_manager;
	std::shared_ptr<SoundImpl> sound_impl;

public:
	category_t get_category() const;
	int get_id() const;

	void play();
	void stop();

private:
	Sound(AudioManager *audio_manager, std::shared_ptr<SoundImpl> sound_impl);

	friend class AudioManager;
};



}
}

#endif
