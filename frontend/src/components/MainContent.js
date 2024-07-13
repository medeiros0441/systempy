import React from 'react';

const MainContent = ({ children }) => {
  return (
    <div id="content">
      <div id="id_alert_container" className="container mx-auto"></div>
      {children}
    </div>
  );
};

export default MainContent;
