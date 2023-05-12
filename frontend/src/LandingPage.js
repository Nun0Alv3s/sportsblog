import React, { useEffect } from 'react';
import Draggable from 'react-draggable';
import { Engine, Render, World, Bodies } from 'matter-js';
import './LandingPage.css';

const LandingPage = () => {
  useEffect(() => {
    const engine = Engine.create();
    const render = Render.create({
      element: document.body,
      engine: engine,
      options: {
        width: 0,
        height: 0,
        background: 'transparent',
        wireframes: false,
      },
    });

    const ball = Bodies.circle(50, 50, 50, {
      restitution: 0.5,
      friction: 0.1,
      density: 0.01,
    });

    World.add(engine.world, [ball]);
    Engine.run(engine);
    Render.run(render);

    return () => {
      Render.stop(render);
      Engine.clear(engine);
      World.clear(engine.world);
    };
  }, []);

  return (
    <div className="landing-page">
      <div className="content">
        <h1>Sportify</h1>
        <p>
          A place to share your thoughts about sports, connect with others, and
          stay updated with the latest news.
        </p>
        <a href="http://localhost:8000/home" className="enter-button">
          Enter Site
        </a>
      </div>
      <Draggable>
        <div className="ball"></div>
      </Draggable>
    </div>
  );
};

export default LandingPage;
