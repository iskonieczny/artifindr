export const initializeValues = (nodes = []) => {
  console.log(nodes)
  nodes.forEach((node) => {
      if (
        node.attributes.type === "button" ||
        node.attributes.name === "provider"
      ) {
        return
      }
      values[node.attributes.name] = node.attributes.value
    }
  )
  setValues( values )
}