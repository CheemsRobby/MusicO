import React from 'react';
import { Card, Typography, Button, Tooltip, Popover } from 'antd';
import { PlayCircleOutlined, HeartOutlined, StarOutlined } from '@ant-design/icons';
import { usePlayer } from '../../contexts/PlayerContext';
import './index.css';

const { Title, Text } = Typography;

const SongCard = ({ song, showExplanation = false, explanation = '' }) => {
  const { playSong } = usePlayer();

  const handlePlay = () => {
    playSong(song);
  };

  const renderExplanation = () => {
    if (!showExplanation || !explanation) return null;

    return (
      <Popover
        content={<Text>{explanation}</Text>}
        title="推荐理由"
        trigger="hover"
      >
        <Button type="text" icon={<StarOutlined />} className="explanation-button">
          查看推荐理由
        </Button>
      </Popover>
    );
  };

  return (
    <Card
      className="song-card"
      cover={
        <div className="song-cover">
          <img
            alt={song.title}
            src={song.cover || '/default-cover.jpg'}
            className="cover-image"
          />
          <div className="cover-overlay">
            <Button
              type="primary"
              shape="circle"
              icon={<PlayCircleOutlined />}
              size="large"
              onClick={handlePlay}
            />
          </div>
        </div>
      }
      actions={[
        <Tooltip title="播放">
          <Button type="text" icon={<PlayCircleOutlined />} onClick={handlePlay} />
        </Tooltip>,
        <Tooltip title="收藏">
          <Button type="text" icon={<HeartOutlined />} />
        </Tooltip>,
        showExplanation && renderExplanation(),
      ].filter(Boolean)}
    >
      <Card.Meta
        title={
          <Title level={5} ellipsis={{ rows: 1 }}>
            {song.title}
          </Title>
        }
        description={
          <Text type="secondary" ellipsis={{ rows: 1 }}>
            {song.artist?.name || '未知艺术家'}
          </Text>
        }
      />
      <div className="song-info">
        <Text type="secondary">
          {song.genre && <span className="genre-tag">{song.genre}</span>}
          {song.duration && (
            <span className="duration">
              {Math.floor(song.duration / 60)}:{String(song.duration % 60).padStart(2, '0')}
            </span>
          )}
        </Text>
      </div>
    </Card>
  );
};

export default SongCard; 