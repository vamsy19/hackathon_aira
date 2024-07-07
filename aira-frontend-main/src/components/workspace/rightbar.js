import React, { useState,useEffect } from 'react';
import { Box, Typography, Tabs, Tab, Button, Divider } from '@mui/material';
import NodeEditor from './nodeEditor';
import NodeConfig from './nodeConfig';
import RunNode from './runNode';
import SuperNodeEditor from './superNode';

const Rightbar = ({ nodes, addOneWayNode, addTwoWayNode, addThreeWayNode, setNodes }) => {
    const [selectedTab, setSelectedTab] = useState(0);
    const [multipleSelected, setMultipleSelected] = useState(false);
    useEffect(() => {
        const selectedNodes = nodes.filter(node => node.selected);
        setMultipleSelected(selectedNodes.length > 1);
    }, [nodes]);

    const handleTabChange = (event, newValue) => {
        setSelectedTab(newValue);
    };



    // console.log(nodes);
    return (
        <Box sx={{ backgroundColor: 'lightblue', height: "100%", padding: 2 }}>
            <Tabs value={selectedTab} onChange={handleTabChange}>
                <Tab label="Nodes" />
                <Tab label="Run" />
            </Tabs>
            {selectedTab === 0 && (
                <Box sx={{ padding: 2 }}>
                    <Typography variant="h6" gutterBottom>
                        New Nodes
                    </Typography>
                    <Button onClick={addOneWayNode}>Add One Way Node</Button>
                    {/* <Button onClick={addTwoWayNode}>Add Two Way Node</Button> */}
                    <Button onClick={addThreeWayNode}>Add Three Way Node</Button>
                    <Box sx={{ marginTop: 2 }}>
                        <Divider />
                    </Box>
                    {multipleSelected?
                        <SuperNodeEditor nodes={nodes.filter(node => node.selected)}></SuperNodeEditor>:null    
                    }
                    <Typography variant="h6" gutterBottom>
                        Edit Node
                    </Typography>
                    {nodes.map((node) => (
                        node.selected && (
                            <Box key={node.id} sx={{ marginTop: 2 }}>
                                <NodeEditor node={node.data} nodes={nodes} setNodes={setNodes} />
                            </Box>
                        )
                    ))}
                    <Box sx={{ marginTop: 2 }}>
                        <Divider />
                    </Box>
                    {nodes.map((node) => (
                        node.selected &&node.type==='oneWay' && (
                            <div>
                                <Typography variant="h6" gutterBottom>
                                   Configure Node
                                </Typography>
                                <Box key={node.id} sx={{ marginTop: 2 }}>
                                    <NodeConfig node={node.data} nodes={nodes} setNodes={setNodes} />
                                </Box>
                            </div>
                        )
                    ))}
                   


                </Box>
            )}
            {selectedTab === 1 && (
                <Box sx={{ padding: 2, height: "100%", }}>
                    <Typography variant="h6" gutterBottom>
                        Run
                    </Typography>

                    {nodes.map((node) => (
                        node.selected && (
                            <Box key={node.id} sx={{ marginTop: 2, height: "100%" }}>
                                <Typography variant="subtitle2" gutterBottom>
                                    {node.name}
                                </Typography>
                                <RunNode node={node}></RunNode>
                            </Box>
                        )
                    ))}
                </Box>
            )}
        </Box>
    );
};

export default Rightbar;