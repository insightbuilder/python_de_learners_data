const App = () => {
  return React.createElement(
    React.Fragment,
    null,
    React.createElement(
      "div",
      {
        style: { height: "500px" },
      },
      React.createElement(ExcalidrawLib.Excalidraw),
    ),
  );
};


function AppElements() {
  const elements = convertToExcalidrawElements([
      {
      type: "rectangle",
      x: 100,
      y: 250,
    },
    {
        type: "ellipse",
        x: 250,
        y: 250,
    },
    {
        type: "diamond",
      x: 380,
      y: 250,
    },
]);
return (
    <div style={{ height: "500px" }}>
      <Excalidraw
        initialData={{
          elements,
          appState: { zenModeEnabled: true, viewBackgroundColor: "#a5d8ff" },
          scrollToContent: true,
        }}
        />
    </div>
  );
}

const excalidrawWrapper = document.getElementById("app");
const root = ReactDOM.createRoot(excalidrawWrapper);
root.render(React.createElement(App));
/* root.render(React.createElement(AppElements)); */
