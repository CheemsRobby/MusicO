import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Typography, Button, Select, Spin, message, Tabs } from 'antd';
import { HeartOutlined, PlayCircleOutlined, StarOutlined } from '@ant-design/icons';
import { useAuth } from '../../contexts/AuthContext';
import { getRecommendations, getTaskStatus } from '../../services/recommendation';
import SongCard from '../../components/SongCard';
import './index.css';

const { Title, Text } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const Recommendation = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [taskId, setTaskId] = useState(null);
  const [recommendationType, setRecommendationType] = useState('hybrid');
  const [limit, setLimit] = useState(10);
  const [usePreferences, setUsePreferences] = useState(true);

  const fetchRecommendations = async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const response = await getRecommendations({
        recommendation_type: recommendationType,
        limit,
        use_preferences: usePreferences,
        refresh: true
      });
      
      if (response.task_id) {
        setTaskId(response.task_id);
        checkTaskStatus(response.task_id);
      } else {
        setRecommendations(response);
        setLoading(false);
      }
    } catch (error) {
      message.error('获取推荐失败');
      setLoading(false);
    }
  };

  const checkTaskStatus = async (taskId) => {
    try {
      const response = await getTaskStatus(taskId);
      if (response.status === 'completed') {
        setRecommendations(response.result.recommendations);
        setTaskId(null);
        setLoading(false);
      } else if (response.status === 'failed') {
        message.error('推荐生成失败');
        setTaskId(null);
        setLoading(false);
      } else {
        setTimeout(() => checkTaskStatus(taskId), 2000);
      }
    } catch (error) {
      message.error('检查任务状态失败');
      setTaskId(null);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, [user, recommendationType, limit, usePreferences]);

  const handleTypeChange = (value) => {
    setRecommendationType(value);
  };

  const handleLimitChange = (value) => {
    setLimit(value);
  };

  const handlePreferencesChange = (checked) => {
    setUsePreferences(checked);
  };

  const getRecommendationTitle = (type) => {
    switch (type) {
      case 'collaborative':
        return '基于用户相似度的推荐';
      case 'content':
        return '基于歌曲特征的推荐';
      case 'hybrid':
        return '混合推荐';
      case 'popular':
        return '热门推荐';
      default:
        return '推荐';
    }
  };

  return (
    <div className="recommendation-page">
      <div className="recommendation-header">
        <Title level={2}>音乐推荐</Title>
        <div className="recommendation-controls">
          <Select
            value={recommendationType}
            onChange={handleTypeChange}
            style={{ width: 200, marginRight: 16 }}
          >
            <Option value="hybrid">混合推荐</Option>
            <Option value="collaborative">协同过滤</Option>
            <Option value="content">基于内容</Option>
            <Option value="popular">热门推荐</Option>
          </Select>
          <Select
            value={limit}
            onChange={handleLimitChange}
            style={{ width: 120, marginRight: 16 }}
          >
            <Option value={5}>显示5首</Option>
            <Option value={10}>显示10首</Option>
            <Option value={20}>显示20首</Option>
          </Select>
          <Button
            type="primary"
            onClick={fetchRecommendations}
            loading={loading}
          >
            刷新推荐
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="loading-container">
          <Spin size="large" />
          <Text>正在生成推荐...</Text>
        </div>
      ) : (
        <div className="recommendation-content">
          <Tabs defaultActiveKey="1">
            <TabPane tab="推荐歌曲" key="1">
              <Row gutter={[16, 16]}>
                {recommendations.map((recommendation) => (
                  <Col xs={24} sm={12} md={8} lg={6} key={recommendation.song_id}>
                    <SongCard
                      song={recommendation}
                      showExplanation={true}
                      explanation={recommendation.explanation}
                    />
                  </Col>
                ))}
              </Row>
            </TabPane>
            <TabPane tab="推荐说明" key="2">
              <Card className="explanation-card">
                <Title level={4}>推荐算法说明</Title>
                <Text>
                  {recommendationType === 'hybrid' && (
                    <p>
                      混合推荐结合了协同过滤和基于内容的推荐方法，为您提供更全面的音乐推荐体验。
                      系统会分析您的听歌历史、评分记录以及相似用户的喜好，同时考虑歌曲的音乐特征，
                      为您推荐可能感兴趣的音乐。
                    </p>
                  )}
                  {recommendationType === 'collaborative' && (
                    <p>
                      协同过滤推荐基于用户相似度，系统会找到与您有相似音乐品味的用户，
                      并推荐他们喜欢但您还未听过的歌曲。这种方法特别适合发现新的音乐。
                    </p>
                  )}
                  {recommendationType === 'content' && (
                    <p>
                      基于内容的推荐分析歌曲的音乐特征，如节奏、能量、情绪等，
                      为您推荐与您喜欢的歌曲在音乐特征上相似的歌曲。
                    </p>
                  )}
                  {recommendationType === 'popular' && (
                    <p>
                      热门推荐基于歌曲的整体评分和播放量，为您推荐平台上最受欢迎的音乐。
                      这是一个发现新音乐的好方法。
                    </p>
                  )}
                </Text>
              </Card>
            </TabPane>
          </Tabs>
        </div>
      )}
    </div>
  );
};

export default Recommendation; 