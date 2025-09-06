body {
  font-family: 'Tajawal', sans-serif;
  background: linear-gradient(135deg, #0b1437, #1e2a78);
  color: white;
  text-align: center;
  margin: 0;
  padding: 0;
}

header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 20px;
}

.logo {
  height: 60px;
}

h1 {
  margin: 0;
  font-size: 32px;
  color: gold;
}

.tag {
  font-size: 14px;
  opacity: 0.9;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
  margin: 30px;
}

.tile {
  background: #1e2a78;
  padding: 16px;
  border-radius: 12px;
  text-decoration: none;
  color: #fff;
  font-weight: bold;
  transition: transform 0.2s, background 0.2s;
}

.tile:hover {
  transform: translateY(-5px);
  background: #2d3a9c;
}

.tile.gold {
  background: gold;
  color: #222;
}

.footer {
  margin-top: 40px;
  padding: 15px;
  font-size: 14px;
  background: #0b1437;
  opacity: .9;
}
