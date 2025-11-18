import { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { text: 'Здравствуйте! Чем я могу вам помочь?', sender: 'bot' },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isFaqVisible, setIsFaqVisible] = useState(false);
  const [activeFaqIndex, setActiveFaqIndex] = useState(null);
  const messagesEndRef = useRef(null);

  const faqData = [
    {
      question: 'Что это за сервис?',
      answer: 'Это умный помощник, созданный для ответов на ваши вопросы в режиме реального времени.',
    },
    {
      question: 'Вопрос?',
      answer: 'Ответ',
    },
    {
      question: 'Вопрос?',
      answer: 'Ответ',
    },
    {
      question: 'Вопрос?',
      answer: 'Ответ',
    },
    {
      question: 'Вопрос?',
      answer: 'Ответ',
    },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (inputValue.trim() === '') return;

    const newMessages = [...messages, { text: inputValue, sender: 'user' }];
    setMessages(newMessages);
    setInputValue('');

    setTimeout(() => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: 'абоба', sender: 'bot' },
      ]);
    }, 1000);
  };

  const handleFaqClick = () => {
    setIsFaqVisible(!isFaqVisible);
    setActiveFaqIndex(null);
  };

  const handleFaqItemClick = (index) => {
    setActiveFaqIndex(activeFaqIndex === index ? null : index);
  };

  return (
    <div className="App">
      <div className="chat-content-wrapper">
        <header className="chatbot-header">
          <h1>Умный помощник</h1>
        </header>

        <main className="chatbot-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message-wrapper ${message.sender}`}>
              <div className="message">{message.text}</div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </main>

        <footer className="chatbot-footer">
          {isFaqVisible && (
            <div className="faq-section">
              {faqData.map((item, index) => (
                <div
                  key={index}
                  className={`faq-item ${activeFaqIndex === index ? 'active' : ''}`}
                  onClick={() => handleFaqItemClick(index)}
                >
                  <div className="faq-question">
                    {item.question}
                    <span>{activeFaqIndex === index ? '−' : '+'}</span>
                  </div>
                  <div className="faq-answer">{item.answer}</div>
                </div>
              ))}
            </div>
          )}
          <div className="faq-button-container">
            <button onClick={handleFaqClick}>
              {isFaqVisible ? 'Скрыть ЧаВо' : 'Просмотреть ЧаВо'}
            </button>
          </div>
          <div className="chatbot-input-area">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Спросите что-нибудь..."
            />
            <button onClick={handleSendMessage}>➤</button>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;